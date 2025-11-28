import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

def add_to_blacklist(token: str, expire_time: int):
    """将令牌加入黑名单"""
    redis_client.setex(f"blacklist:{token}", expire_time, "true")

def is_token_blacklisted(token: str) -> bool:
    """检查令牌是否在黑名单中"""
    return redis_client.exists(f"blacklist:{token}")