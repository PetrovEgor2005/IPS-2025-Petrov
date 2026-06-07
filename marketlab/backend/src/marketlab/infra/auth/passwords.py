from passlib.context import CryptContext
#в качестве функции хеширования взял bcrypt, особенностью которой является случайность добавочных байтов, 
#а также она намеренно медленная, что хорошо для безопасности, идеально подхожит для паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#в данной функции формируется хеш, который потом будет храниться в базе данных с паролями
def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

#здесь происходит декодирование пароля и его сравнение с хешом
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
