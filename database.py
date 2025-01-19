# E:\work\metahuman-stream\langchain\jiyi\database.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from datetime import datetime

# ---------- 初始化 SQLAlchemy ----------
# SQLAlchemy 基础类
Base = declarative_base()

# ---------- 定义数据模型 ----------
class ChatHistory(Base):
    """
    定义 'chat_history' 表的结构
    """
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    user_id = Column(String(50), index=True, nullable=False)    # 用户 ID
    message = Column(Text, nullable=False)                     # 用户消息
    response = Column(Text, nullable=False)                    # AI 回复
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)  # 时间戳

# ---------- 配置数据库引擎 ----------
# SQLite 数据库，数据库文件名为 'chat_history.db'
DATABASE_URL = 'sqlite:///chat_history.db'
engine = create_engine(DATABASE_URL, echo=False)

# 创建所有表（如果表不存在的话）
Base.metadata.create_all(engine)

# 创建数据库会话类
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ---------- 数据库依赖 ----------
def get_db() -> Session:
    """
    获取数据库会话，确保请求结束后关闭连接
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- 实现数据库操作方法 ----------
def add_chat_history(db: Session, user_id: str, message: str, response: str):
    """
    添加一条聊天记录到数据库
    """
    try:
        chat = ChatHistory(user_id=user_id, message=message, response=response)
        db.add(chat)  # 添加记录到会话
        db.commit()   # 提交会话到数据库
        db.refresh(chat)  # 刷新记录（获取插入后的 ID）
        return chat
    except Exception as e:
        db.rollback()  # 出现错误时回滚
        raise e

def get_chat_history(db: Session, user_id: str, limit: int = 5):
    """
    从数据库中获取某用户的聊天记录，按时间倒序排列
    """
    return db.query(ChatHistory) \
        .filter(ChatHistory.user_id == user_id) \
        .order_by(ChatHistory.timestamp.desc()) \
        .limit(limit) \
        .all()
