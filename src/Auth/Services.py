from sqlmodel import select
from src.Auth.Schema import LoginUser,CreateUser
from src.DB.Models import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.Auth.utils import generate_password_hash
from fastapi import Depends, HTTPException
from src.DB.__init__ import get_session

class UserService:
    def __init__(self,session:AsyncSession):
        self.session=session
      
    async def Create_User(self,user_details:CreateUser):
        user=User(**user_details.model_dump())
        user.password_hash=generate_password_hash(user_details.password)
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            raise HTTPException(status_code=400,detail=str(e))

    async def getUserByEmail(self,email:str):
        statement=select(User).where(User.email==email)
        try:
            result=await self.session.execute(statement)
            return result.scalars().first()
        except Exception as e:
            raise HTTPException(status_code=400,detail=str(e))   
            
    async def updateUser(self,user:User,user_data:dict):
        for k,v in user_data.items():
            setattr(user,k,v)
        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            raise HTTPException(status_code=400,detail=str(e))
        
    async def UserExists(self,email:str)->bool:
        try:
            user=await self.getUserByEmail(email)
            if user is None:
                return False
            return True
        except Exception as e:
            raise HTTPException(status_code=400,detail=str(e))
    
async def getSession(session: AsyncSession=Depends(get_session))->UserService:
    return UserService(session)
   