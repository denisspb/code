namespace cpp com.test

struct Param1 {
    1: required i32 userId,
    4: optional i32 userType,
    5: required i32 userNum = 3
}

service Calculator {
    i32 addF(1:i32 num1, 2: optional i32 num2, 3: optional i32 num3)
    i32 delF(1:i32 num1, 2: optional i32 num2, 3: i32 num3)
}