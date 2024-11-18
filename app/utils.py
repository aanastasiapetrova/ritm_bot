from app import db


async def check_subscription(user_id) -> bool:
    user_info = await db.check_user(user_id=user_id)
    
    if user_info:
        is_sub_active = user_info[-1]
        if is_sub_active:
            return True
    
    return False
