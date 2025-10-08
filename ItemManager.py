import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# 物品类
class Item:
    def __init__(self, name, description, contact):
        # 物品名称
        self.name = name
        # 物品描述
        self.description = description
        # 联系人信息
        self.contact = contact

# 物品管理类
class ItemManager:
    def __init__(self):
        # 用于存储物品列表
        self.items = []
        # 数据文件路径
        self.file_path = "items.json"
        # 尝试从文件加载数据
        self.load_items()
        # 物品数量
        self.itemNum = len(self.items)

    def add_item(self, item):
        """添加物品"""
        self.items.append(item)
        self.save_items()
        return True


    def delete_item(self, index):
        """删除物品"""
        if self.itemNum > 0 and index >= 0 and index < self.itemNum:
            del self.items[index]
            self.save_items()
            return True
        return False

    def get_items(self):
        """获取物品列表"""
        return self.items

    def find_item(self, keyword):
        """查找物品"""
        result = []
        for item in self.items:
            if (keyword.lower() in item.name.lower() or 
                keyword.lower() in item.description.lower() or 
                keyword.lower() in item.contact.lower()):
                result.append(item)
        return result

    def save_items(self):
        """保存物品到文件"""
        data = []
        for item in self.items:
            data.append({
                "name": item.name,
                "description": item.description,
                "contact": item.contact
            })
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_items(self):
        """从文件加载物品"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item_data in data:
                        item = Item(
                            item_data["name"],
                            item_data["description"],
                            item_data["contact"]
                        )
                        self.items.append(item)
            except Exception as e:
                print(f"加载数据出错: {e}")

# GUI 类
class ItemResurrectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("物品“复活”软件")
        self.root.geometry("800x600")
        self.item_manager = ItemManager()

        # 创建界面组件
        self.create_widgets()
        # 刷新物品列表
        self.refresh_item_list()

    def create_widgets(self):
        # 左侧：添加物品区域
        left_frame = tk.Frame(self.root, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left_frame, text="物品名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = tk.Entry(left_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        tk.Label(left_frame, text="物品描述:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.description_entry = tk.Entry(left_frame, width=30)
        self.description_entry.grid(row=1, column=1, pady=5)

        tk.Label(left_frame, text="联系人信息:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.contact_entry = tk.Entry(left_frame, width=30)
        self.contact_entry.grid(row=2, column=1, pady=5)

        add_button = tk.Button(left_frame, text="添加物品", command=self.add_item)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # 中间：物品列表区域
        middle_frame = tk.Frame(self.root, padx=10, pady=10)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(middle_frame, text="物品列表:").pack(anchor=tk.W, pady=5)

        columns = ("序号", "物品名称", "物品描述", "联系人信息")
        self.tree = ttk.Treeview(middle_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        delete_button = tk.Button(middle_frame, text="删除选中物品", command=self.delete_item)
        delete_button.pack(anchor=tk.W, pady=5)

        # 右侧：查找区域
        right_frame = tk.Frame(self.root, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(right_frame, text="查找关键词:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.search_entry = tk.Entry(right_frame, width=20)
        self.search_entry.grid(row=0, column=1, pady=5)

        search_button = tk.Button(right_frame, text="查找", command=self.search_item)
        search_button.grid(row=0, column=2, pady=5)

        refresh_button = tk.Button(right_frame, text="刷新列表", command=self.refresh_item_list)
        refresh_button.grid(row=1, column=0, columnspan=3, pady=5)

    def add_item(self):
        """添加物品"""
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        contact = self.contact_entry.get().strip()

        if not name or not description or not contact:
            messagebox.showerror("错误", "物品名称、描述和联系人信息不能为空！")
            return

        item = Item(name, description, contact)
        if self.item_manager.add_item(item):
            messagebox.showinfo("成功", "物品添加成功！")
            self.name_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.contact_entry.delete(0, tk.END)
            self.refresh_item_list()

    def delete_item(self):
        """删除物品"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选中要删除的物品！")
            return

        item_index = int(self.tree.item(selected_item[0], "values")[0]) - 1
        if self.item_manager.delete_item(item_index):
            messagebox.showinfo("成功", "物品删除成功！")
            self.refresh_item_list()

    def refresh_item_list(self):
        """刷新物品列表"""
        # 清空树状视图
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 重新加载物品列表
        items = self.item_manager.get_items()
        for i, item in enumerate(items):
            self.tree.insert("", tk.END, values=(i + 1, item.name, item.description, item.contact))

    def search_item(self):
        """查找物品"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showinfo("提示", "请输入查找关键词！")
            return

        # 清空树状视图
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 查找物品
        items = self.item_manager.find_item(keyword)
        for i, item in enumerate(items):
            self.tree.insert("", tk.END, values=(i + 1, item.name, item.description, item.contact))

# 主函数
if __name__ == "__main__":
    root = tk.Tk()
    app = ItemResurrectionApp(root)
    root.mainloop()