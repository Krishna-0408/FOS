from pydantic import BaseModel, EmailStr, field_validator, model_validator
import re


class UserSignup(BaseModel):
    name: str
    phone: str
    email: EmailStr
    address: str
    place: str
    city: str
    district: str
    pincode: str
    password: str
    confirm_password: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if len(value.strip()) < 3:
            raise ValueError("Name must be at least 3 characters.")
        return value.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        return value

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value):
        if not re.fullmatch(r"\d{6}", value):
            raise ValueError("Pincode must contain exactly 6 digits.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#^()_+=-])[A-Za-z\d@$!%*?&#^()_+=-]{8,}$'

        if not re.match(pattern, value):
            raise ValueError(
                "Password must be at least 8 characters and contain an uppercase letter, lowercase letter, number, and special character."
            )
        return value

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and Confirm Password do not match.")
        return self


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#^()_+=-]).{8,}$'

        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain uppercase, lowercase, number and special character."
            )

        return value

    @model_validator(mode="after")
    def password_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError(
                "Password and Confirm Password do not match."
            )

        return self