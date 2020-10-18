from drivermanager import DriverManager
from icooon_mono import Scraping_icooon_mono, Size, Ext, Category
import time

if __name__ == "__main__":
    dm = DriverManager(driver_dir=".", driver_version="86.0.4240.22",)
    # 保存場所
    path = "C:\\Users\\shindy\\Downloads\\icooon-mono\\"
    # カテゴリ
    category = Category.health
    # 拡張子
    ext = Ext.png
    # 画像の解像度
    size = Size.px48
    # 色(rgb)
    color = (75, 75, 75)

    print("<<< Download config >>>")
    print(f"Path: {path}")
    print(f"Category: {category.name}")
    print(f"Extension: {ext.name}")
    print(f"Size: {size.name}")
    print(f"Color: {color}")
    print("<<< Download config >>>\n")

    start = time.time()
    
    service = Scraping_icooon_mono(dm, path)
    print("icon listup...")
    icon_ids = sorted(set(service.get_icon_ids(Category.health)))
    with open("icon_ids.csv", "w") as f:
        [f.write(f"{icon_id},{icon_name}\n") for icon_id, icon_name in icon_ids]

    print(f"<<< Download Start... ({len(icon_ids)})>>>")
    for icon_id, icon_name in icon_ids:
        print(f"id: {icon_id}, name: {icon_name}")
        service.download_icon(icon_id, ext, size, color)
    print(f"<<< Download End... ({len(icon_ids)})>>>")

    print(f"time: {time.time() - start}")
    
    del service
    print(f"終了するには何かキーを入力してください...")
    input()
