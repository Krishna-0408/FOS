from app.core.security import hash_password, verify_password

password = "Krishna@123"

hashed = hash_password(password)

print("Original Password :", password)
print("Hashed Password   :", hashed)

print("Verify :", verify_password(password, hashed))