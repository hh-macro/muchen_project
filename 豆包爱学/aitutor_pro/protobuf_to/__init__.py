from .addressbook import GetByUserInit
from .addressbook_two import GetByUserInitTwo
"""
protoc -I . --python_betterproto_out= addressbook.proto  ---- 使用 protoc 编译器将 .proto 文件编译为python代码
"""