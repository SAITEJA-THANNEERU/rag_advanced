import os
import jwt

from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

JWT_SECRET = os.getenv("RAG_INTERNAL_JWT_SECRET")

JWT_ALGORITHM = "HS256"
EXPECTED_ISSUER = "factoryops-express"
EXPECTED_AUDIENCE = "factoryops-rag"

bearer_scheme = HTTPBearer(auto_error=False)


if not JWT_SECRET:
    raise RuntimeError("RAG_INTERNAL_JWT_SECRET is missing")


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization token"
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            issuer=EXPECTED_ISSUER,
            audience=EXPECTED_AUDIENCE,
            options={
                "require": [
                    "exp", "iat", "sub", "role",
                    "factory_id", "iss", "aud"
                ]
            }
        )

        role = payload["role"]
        factory_id = payload["factory_id"]

        allowed_roles = {
            "SUPER_ADMIN",
            "ADMIN",
            "MANAGER_SUPERVISOR",
            "PRODUCTION_PLANNER",
            "TECHNICIAN"
        }

        if role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Unauthorized role")

        if role != "SUPER_ADMIN" and not factory_id:
            raise HTTPException(status_code=403, detail="Factory assignment required")

        return {
            "user_id": payload["sub"],
            "role": role,
            "factory_id": factory_id
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")