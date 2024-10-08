from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import List, Optional
from pydantic import BaseModel
from BlogFastAPI.app.models.user import User
