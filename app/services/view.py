from datetime import datetime, timedelta

from celery.backends import redis
from redis import Redis
from fastapi import Depends, HTTPException, Request, BackgroundTasks

from ..api.deps import get_current_active_user

CommonDeps = Depends(get_current_active_user)


# Redis key patterns , we will add post id after second ':'
POST_PREVIEW_PREFIX = "post:preview:"
POST_DETAIL_PREFIX = "post:detail:"


