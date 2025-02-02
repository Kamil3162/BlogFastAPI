import typing
from datetime import datetime, timezone
from itertools import count, groupby

from sqlalchemy import exc, desc, select, func, extract
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ...models.post import Post, PostVote, PostView
from ...models.user import User
from ...models.category import PostCategory, PostCategories
from ...schemas.post import PostCreate, PostUpdate, PostInfo
from ...core.enums import VoteType

class PostRepository:
    def __init__(self, db: Session):
        self._db = db
        self._model = Post
        self._view = PostView

    def get_by_id(self, post_id: int):
        """
            Retrieve a post by its ID using SQLAlchemy 2.0 style querying.

            Args:
                post_id (int): The unique identifier of the post

            Returns:
                Optional[Post]: The post instance if found, None otherwise

            Example:
                >>> post = post_repository.get_by_id(1)
                >>> print(post.title)
        """
        stmt = select(self._model).where(self._model.id == post_id)
        result = self._db.execute(stmt)
        modern_way = result.scalar_one_or_none()

        return modern_way

    def get_by_title(self, db: Session, title: str) -> Post:
        """
           Search for a post by its title using case-insensitive partial matching.

           Args:
               db (Session): SQLAlchemy database session
               title (str): Full or partial title to search for

           Returns:
               Optional[Post]: First matching post or None if not found

           Example:
               >>> post = post_repository.get_by_title(db, "Python")
               >>> if post:
               >>>     print(f"Found: {post.title}")
           """
        post = db.query(Post).filter(Post.title.ilike(f'%{title}%')).first()
        return post

    def get_by_category(self, db: Session, category_id):
        """
            Retrieve all posts in a specific category.

            Args:
                db (Session): SQLAlchemy database session
                category_id (int): Name of the category to filter by

            Returns:
                List[Post]: List of posts in the specified category

            Example:
                >>> tech_posts = post_repository.get_by_category(db, 3)
                >>> print(f"Found {len(tech_posts)} posts")
        """
        stmt = (
            select(Post)
            .join(PostCategories, Post.id == PostCategories.post_id)
            .join(PostCategory, PostCategories.category_id == PostCategory.id)
            .where(PostCategory.id == category_id)
            .order_by(
                Post.created_at.desc())  # Optional: order by creation date
            .limit(10)  # Optional: limit number of results
        )

        result = db.execute(stmt)
        posts = result.scalars().all()
        return posts

    def create(self, post_data: PostCreate):
        """
            Create a new post in the database.

            Args:
                post_data (PostCreate): Pydantic model containing post creation data
                    Required fields:
                    - title: str
                    - content: str
                    - photo_url: Optional[str]
                    - owner_id: int

            Returns:
                Post: Newly created post instance

            Example:
                >>> new_post = PostCreate(title="New Post", content="Content", owner_id=1)
                >>> post = post_repository.create(new_post)
            """
        print("create function")

        db_post = Post(
            title=post_data.title,
            content=post_data.content,
            photo_url=post_data.photo_url,
            owner_id=post_data.owner_id
        )

        self._db.add(db_post)
        self._db.commit()

        return db_post

    def update(self, post_instance: Post, post_data: PostUpdate):
        """
        Update an existing post with new data.

        Args:
            post_instance (Post): Existing post instance to update
            post_data (PostUpdate): Pydantic model containing update data

        Returns:
            Post: Updated post instance

        Example:
            >>> update_data = PostUpdate(title="Updated Title")
            >>> updated_post = post_repository.update(post, update_data)
    """

        update_data = post_data.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        for key, value in update_data.items():
            if hasattr(post_instance, key):
                setattr(post_instance, key, value)

        self._db.add(post_instance)
        self._db.commit()
        self._db.refresh(post_instance)

        return post_instance

    def get_posts(self, db: Session):
        """
            Retrieve all posts from the database.

            Args:
                db (Session): SQLAlchemy database session

            Returns:
                List[Post]: All posts in the database

            Example:
                >>> all_posts = post_repository.get_posts(db)
                >>> print(f"Total posts: {len(all_posts)}")
        """
        posts = db.query(Post).all()
        return posts

    def get_posts_range(self, db: Session, skip: int = 0, limit: int = 10):
        """
           Retrieve a paginated list of posts.

           Args:
               db (Session): SQLAlchemy database session
               skip (int, optional): Number of records to skip. Defaults to 0
               limit (int, optional): Maximum number of records to return. Defaults to 10

           Returns:
               List[Post]: Paginated list of posts

           Example:
               >>> posts = post_repository.get_posts_range(db, skip=20, limit=10)
               >>> # Gets posts 21-30
       """
        posts = db.query(self._model).offset(skip).limit(limit).all()
        return posts

    def get_newest_post(self, db: Session):
        """
            Retrieve the most recently created post.

            Args:
                db (Session): SQLAlchemy database session

            Returns:
                Optional[Post]: Most recent post or None if no posts exist

            Example:
                >>> latest = post_repository.get_newest_post(db)
                >>> if latest:
                >>>     print(f"Latest post: {latest.title}")
        """
        newest_post = db.query(self._model).order_by(
            desc(self._model.created_at).first()
        )
        return newest_post

    def delete_post(self, post_id):
        """
            Delete a post from the database.

            Args:
                post_id (int): ID of the post being voted on

            Returns:
                bool : Success or failure

            Example:
                >>> post_repository.delete_post(post_id)
        """
        result = self._db.query(Post).filter(Post.id == post_id).delete()

        return bool(result)

    # functions responsible for get vote instances
    def upvote_create(self, user_id, post_id, vote_type: VoteType):
        post_vote = PostVote(
            post_id=post_id,
            user_id=user_id,
            vote_type=vote_type,
        )

        self._db.add(post_vote)
        self._db.commit()

    def upvote_delete(self, post_id, user_id):
        post_vote = self._db.query(PostVote).where(
            PostVote.post_id == post_id,
            PostVote.user_id == user_id
        ).one()

        self._db.delete(post_vote)
        self._db.commit()

    def upvote_update(self, post_id, user_id, vote_type: VoteType):
        post_vote = self._db.query(PostVote).where(
            PostVote.post_id == post_id,
            PostVote.user_id == user_id
        ).one()

        post_vote.vote_type = vote_type

        self._db.refresh(post_vote)
        self._db.commit()

        return post_vote

    def get_vote_instance(self, user_id, post_id):
        stmt = select(PostVote).where(
            PostVote.post_id == post_id,
            PostVote.user_id == user_id
        )

        return self._db.scalars(stmt).first()

    # functions responsible for operate on views
    def create_post_view(
        self,
        post_id: int,
        user_id: typing.Optional[int] = None,
        user_ip: str = "127.0.0.1"
    ):
        post_view = PostView(
            post_id=post_id,
            user_id=user_id,
            viewer_ip=user_ip,
            viewed_at=datetime.now(timezone.utc),
        )

        self._db.add(post_view)
        self._db.commit()

        return post_view

    def post_up_view(
        self,
        post_id: int,
        user_id: typing.Optional[int] = None,
        user_ip: str = "127.0.0.1"
    ):
        pass

    def get_total_views(self, post_id: int) -> int:
        """
        Gets the total view count for a post.
        Uses SQLAlchemy's select statement for type safety.
        """
        query = select(func.count()).select_from(PostView).where(
            PostView.post_id == post_id)
        result = self._db.execute(query)
        return result.scalar_one()

    def get_generated_views(self, user: id):
        """
            Gets the total view count for a user.
            FUnction generate a result for owner using all created posts.
            Result is broke on months and return total views in each month.

            Params:
                user (int): ID of the user

            Returns:
                - dict[str, int]: Total view count
        """
        query = select(
            extract("month", PostView.viewed_at).label("month"),
            func.count().label("total_views")
        ).select_from(PostView) \
         .join(Post, Post.owner_id == user.id) \
         .where(Post.owner_id == user.id) \
         .group_by(
            extract("month", PostView.viewed_at)
        )

        result = self._db.execute(query)
        rows = result.all()
        return dict(rows)


    def get_post_info_by_user(self, user_id: int):
        """
        Gets posts information with view counts for a specific user.

        Args:
            db (Session): Database session
            user_id (int): ID of the user whose posts to retrieve

        Returns:
            List of tuples containing post information and view counts
        """
        query = (
            select(
                Post.id,
                Post.title,
                Post.content,
                Post.created_at,
                func.count(PostView.id).label('view_count')
            )
            .join(PostView, Post.id == PostView.post_id,
                  isouter=True)  # Left join to include posts with no views
            .where(Post.owner_id == user_id)
            .group_by(Post.id, Post.title, Post.content, Post.created_at)
        )

        result = self._db.execute(query)
        data = result.mappings().all()
        return [PostInfo(**row) for row in data]

    def get_views_by_months(self, post_id):
        """
           Counts post views grouped by month for a given post.

           This query extracts the month from the viewed_at timestamp,
           groups the results by that month, and counts views for each month.

           Args:
               post_id: The ID of the post to analyze

           Returns:
               A dictionary where keys are month numbers (1-12) and values are view counts
       """
        query = (
            select(
                extract('month', PostView.viewed_at).label('month'),
                func.count(PostView.id).label('view_count')  # Count views
            )
            .where(PostView.post_id == post_id)
            .group_by(extract('month', PostView.viewed_at))
            .order_by('month')  # Optional: order results by month
        )

        try:
            # Execute the query and process results
            result = self._db.execute(query)

            # Convert results to a dictionary for easy access
            monthly_views = {
                int(month): count
                for month, count in result.fetchall()
            }

            return monthly_views
        except Exception as e:
            raise e

    def get_monthly_views_by_user(self, user_id: int):
        """
            Generate accumulated views for each month for a given user.

            Function generate accumulated views for each month which post creator
            generate during create a brand new post or existing views

            Returns:
                Dict[id: [dict]] where:
                    - id: particular post id
                    - dict: { month: views}

            Example:
                {
                    1: {"January" : 32321, "February": 32132132}
                }
        """
        query = select(
            PostView.post_id,
            extract('month', PostView.viewed_at).label('month'),
            extract('year', PostView.viewed_at).label('year'),
            Post.owner_id,
            # Added this since you're using it in the return dict
            func.count(PostView.id).label("view_count"),
        ).select_from(PostView) \
         .join(Post, Post.id == PostView.post_id) \
         .join(User, User.id == Post.owner_id) \
         .where(PostView.user_id == user_id) \
         .group_by(
            extract('month', PostView.viewed_at),
            extract('year', PostView.viewed_at),
            PostView.post_id,
            Post.owner_id  # Added to group by since it's in select
        )

        result = self._db.execute(query)  # Assuming async
        rows = result.all()

        return [
            {
                "month": int(row.month),
                "year": int(row.year),
                "post_id": row.post_id,
                "owner_id": row.owner_id,
                "view_count": row.view_count
            }
            for row in rows
        ]

    def get_global_views_by_months(self) -> typing.Dict[int, int]:
        """
        Calculates total views across all posts, grouped by month.

        This function aggregates view data from every post in the system to give you
        a complete picture of platform engagement over time. It uses the same monthly
        grouping logic as get_views_by_months, but removes the post_id filter to
        include all posts.

        Returns:
            Dict[int, int]: A dictionary where:
                - Keys are month numbers (1-12)
                - Values are the total view counts across all posts for that month

        Example:
            {
                1: 15000,  # January had 15,000 total views
                2: 17200,  # February had 17,200 total views
                ...
            }
        """
        # Build our query to aggregate views across all posts
        query = (
            select(
                # Extract month from the timestamp for grouping
                extract('month', PostView.viewed_at).label('month'),
                # Count total views across all posts
                func.count(PostView.id).label('view_count')
            )
            # Group by month to get monthly totals
            .group_by(extract('month', PostView.viewed_at))
            # Order results by month for consistency
            .order_by('month')
        )

        try:
            # Execute our query and fetch results
            result = self._db.execute(query)

            # Transform the results into an easy-to-use dictionary
            monthly_views = {
                int(month): count
                for month, count in result.fetchall()
            }

            return monthly_views

        except Exception as e:
            raise e

    def get_global_views_by_months_detailed(self) -> typing.Dict[str, typing.Dict[str, int]]:
        """
        Provides a detailed breakdown of global views including year and month.

        This enhanced version gives you a more complete picture by including the year
        in the analysis, allowing you to track long-term trends and year-over-year
        comparisons.

        Returns:
            A nested dictionary with years and months, showing views for each period.
            Format: {year: {month: view_count}}

        Example:
            {
                "2024": {
                    "1": 15000,  # January 2024
                    "2": 17200   # February 2024
                },
                "2023": {
                    "12": 14500  # December 2023
                }
            }
        """
        query = (
            select(
                # Extract both year and month for detailed grouping
                extract('year', PostView.viewed_at).label('year'),
                extract('month', PostView.viewed_at).label('month'),
                func.count(PostView.id).label('view_count')
            )
            .group_by(
                extract('year', PostView.viewed_at),
                extract('month', PostView.viewed_at)
            )
            # Order by year and month for chronological organization
            .order_by('year', 'month')
        )

        try:
            result = self._db.execute(query)

            views_by_year = {}

            for year, month, count in result.fetchall():
                year_str = str(int(year))
                month_str = str(int(month))

                # Initialize year dictionary if it doesn't exist
                if year_str not in views_by_year:
                    views_by_year[year_str] = {}

                # Add the month's view count
                views_by_year[year_str][month_str] = count

            return views_by_year

        except Exception as e:
            raise e

    def get_platform_analytics(self) -> dict[str, typing.Union[dict[str, int], int]]:
        """
        Generate platform-wide analytics for post views and revenue.

        Aggregates views across all posts and calculates total platform revenue.
        Provides both monthly breakdown and total aggregate views.

        Returns:
            dict: Platform analytics with the following structure:
                {
                    "monthly_totals": {
                        "YYYY-MM": int,  # Views per month
                        ...
                    },
                    "total_views": int  # Total views across all posts
                }

        Raises:
            SQLAlchemyError: If database query fails
            ValueError: If data aggregation fails

        Example:
            >>> analytics = post_repository.get_platform_analytics()
            >>> analytics
            {
                "monthly_totals": {
                    "2024-01": 1000,
                    "2024-02": 1500
                },
                "total_views": 2500
            }
        """
        try:
            monthly_totals = self.get_global_views_by_months()

            return {
                "monthly_totals": monthly_totals,
                "total_views": sum(monthly_totals.values())
            }
        except Exception as e:
            raise e