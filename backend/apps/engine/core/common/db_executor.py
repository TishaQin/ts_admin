# core/common/db_executor.py
from django.db import connection

def execute_sql(sql, params=None):
    """执行 SQL 查询，支持参数化查询"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params or [])
            if cursor.description:  # 如果是查询操作，返回结果
                columns = [col[0] for col in cursor.description]
                results = cursor.fetchall()
                return [dict(zip(columns, row)) for row in results]
            return None  # 如果是数据更新操作，返回 None
    except Exception as e:
        print(f"执行 SQL 时出错: {e}")
        raise  # 重新抛出异常以便上层处理
