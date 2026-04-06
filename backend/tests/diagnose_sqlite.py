import sqlite3
import os

# 数据库路径
db_path = r'E:\pythonProject\CathyHackathon\backend\db.sqlite3'

if not os.path.exists(db_path):
    print(f"数据库文件不存在: {db_path}")
    exit(1)

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("SQLite 数据库诊断")
print("=" * 60)

# 1. 检查表是否存在
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%survey%'")
tables = cursor.fetchall()
print("\n问卷相关的表:")
for table in tables:
    print(f"  - {table[0]}")

# 2. 检查 SurveyResponse 数据
cursor.execute("SELECT COUNT(*) FROM surveys_surveyresponse")
survey_count = cursor.fetchone()[0]
print(f"\n问卷总数: {survey_count}")

if survey_count > 0:
    cursor.execute("""
        SELECT id, dish_id, rating, miles_awarded, created_at 
        FROM surveys_surveyresponse 
        LIMIT 5
    """)
    surveys = cursor.fetchall()
    print("\n前 5 条问卷:")
    for survey in surveys:
        print(f"  ID: {survey[0]}, 菜品ID: {survey[1]}, 评分: {survey[2]}, 已发里数: {survey[3]}")

# 3. 检查 PointTransaction 数据
cursor.execute("SELECT COUNT(*) FROM surveys_pointtransaction")
transaction_count = cursor.fetchone()[0]
print(f"\n积分交易总数: {transaction_count}")

if transaction_count > 0:
    cursor.execute("""
        SELECT id, survey_id, miles, description 
        FROM surveys_pointtransaction 
        LIMIT 5
    """)
    transactions = cursor.fetchall()
    print("\n前 5 条积分交易:")
    for trans in transactions:
        print(f"  ID: {trans[0]}, 问卷ID: {trans[1]}, 积分: {trans[2]}, 描述: {trans[3]}")

# 4. 检查外键约束
cursor.execute("PRAGMA foreign_keys")
fk_status = cursor.fetchone()[0]
print(f"\n外键约束状态: {'启用' if fk_status else '禁用'}")

# 5. 检查 PointTransaction 的外键定义
cursor.execute("PRAGMA foreign_key_list(surveys_pointtransaction)")
foreign_keys = cursor.fetchall()
print("\nsurveys_pointtransaction 的外键:")
for fk in foreign_keys:
    print(f"  列: {fk[3]} -> 表: {fk[2]}, ON DELETE: {fk[5]}")

# 6. 测试删除（如果有数据）
if survey_count > 0:
    print("\n" + "=" * 60)
    print("测试删除功能")
    print("=" * 60)
    
    # 获取第一条问卷的 ID
    cursor.execute("SELECT id FROM surveys_surveyresponse LIMIT 1")
    test_id = cursor.fetchone()[0]
    print(f"\n准备删除问卷 ID: {test_id}")
    
    # 检查关联的积分交易
    cursor.execute("SELECT COUNT(*) FROM surveys_pointtransaction WHERE survey_id = ?", (test_id,))
    related_count = cursor.fetchone()[0]
    print(f"关联的积分交易: {related_count} 条")
    
    # 询问是否执行删除
    choice = input("\n是否执行删除测试？(y/n): ").strip().lower()
    
    if choice == 'y':
        try:
            # 启用外键约束
            cursor.execute("PRAGMA foreign_keys = ON")
            
            # 删除问卷（应该自动级联删除积分交易）
            cursor.execute("DELETE FROM surveys_surveyresponse WHERE id = ?", (test_id,))
            conn.commit()
            
            print(f"✅ 成功删除问卷 ID: {test_id}")
            
            # 验证级联删除
            cursor.execute("SELECT COUNT(*) FROM surveys_pointtransaction WHERE survey_id = ?", (test_id,))
            remaining = cursor.fetchone()[0]
            print(f"删除后剩余的关联积分交易: {remaining}")
            
            if remaining == 0:
                print("✅ 级联删除成功")
            else:
                print("⚠️  警告: 仍有关联的积分交易未被删除")
                
        except Exception as e:
            print(f"❌ 删除失败: {e}")
            conn.rollback()
    else:
        print("已取消删除测试")

conn.close()
print("\n数据库连接已关闭")
