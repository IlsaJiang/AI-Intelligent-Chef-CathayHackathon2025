import json
import os

os.chdir(r'e:\pythonProject\CathyHackathon\frontend\src\i18n')

# 读取所有文件
files = ['zh.json', 'zh-HK.json', 'en.json']
data = {f: json.load(open(f, 'r', encoding='utf-8')) for f in files}

print("=" * 80)
print("i18n 文件深度检查")
print("=" * 80)

# 检查顶层键
print("\n1. 顶层键检查:")
zh_keys = set(data['zh.json'].keys())
hk_keys = set(data['zh-HK.json'].keys())
en_keys = set(data['en.json'].keys())

print(f"  zh.json: {len(zh_keys)} 个键")
print(f"  zh-HK.json: {len(hk_keys)} 个键")
print(f"  en.json: {len(en_keys)} 个键")
print(f"  ✅ 顶层键{'一致' if zh_keys == hk_keys == en_keys else '不一致'}")

# 检查嵌套对象的键
print("\n2. 检查重要嵌套对象的键一致性:")

nested_objects = ['chat', 'aichef', 'feedback', 'survey', 'preselectPage', 'common', 'allergens']

for obj_name in nested_objects:
    if obj_name in data['zh.json'] and isinstance(data['zh.json'][obj_name], dict):
        zh_nested = set(data['zh.json'][obj_name].keys())
        hk_nested = set(data['zh-HK.json'].get(obj_name, {}).keys()) if isinstance(data['zh-HK.json'].get(obj_name), dict) else set()
        en_nested = set(data['en.json'].get(obj_name, {}).keys()) if isinstance(data['en.json'].get(obj_name), dict) else set()
        
        is_same = zh_nested == hk_nested == en_nested
        status = "✅" if is_same else "⚠️"
        print(f"  {status} {obj_name}: zh={len(zh_nested)}, hk={len(hk_nested)}, en={len(en_nested)}")
        
        if not is_same:
            missing_in_hk = zh_nested - hk_nested
            missing_in_en = zh_nested - en_nested
            if missing_in_hk:
                print(f"      hk 缺少: {sorted(missing_in_hk)}")
            if missing_in_en:
                print(f"      en 缺少: {sorted(missing_in_en)}")

print("\n" + "=" * 80)
print("检查完成!")
print("=" * 80)
