import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from puller import concurrent_search
from downloader import download_as_md

class DownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("博客下载助手 (目前支持CSDN/博客园/先知)")
        self.root.geometry("1000x700")
        self.setup_ui()
        
    def setup_ui(self):
        search_frame = tk.LabelFrame(self.root, text="搜索配置", padx=10, pady=10)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(search_frame, text="关键词:").pack(side=tk.LEFT)
        self.kw_entry = tk.Entry(search_frame, width=30)
        self.kw_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(search_frame, text="搜索页数:").pack(side=tk.LEFT, padx=5)
        self.pg_entry = tk.Entry(search_frame, width=5)
        self.pg_entry.insert(0, "1")
        self.pg_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="开始搜索", command=self.on_search_click, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=20)

        path_frame = tk.Frame(self.root, padx=10)
        path_frame.pack(fill=tk.X, padx=10)
        tk.Label(path_frame, text="Chrome 路径:").pack(side=tk.LEFT)
        self.browser_entry = tk.Entry(path_frame)

        # 浏览器路径输入，可根据本地电脑情况修改默认值。
        self.browser_entry.insert(0, r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        self.browser_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(path_frame, text="选择路径", command=self.select_browser).pack(side=tk.LEFT)

        columns = ("site", "title", "url", "status")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("site", text="平台")
        self.tree.heading("title", text="标题")
        self.tree.heading("url", text="文章链接")
        self.tree.heading("status", text="状态")
        self.tree.column("site", width=80, anchor=tk.CENTER)
        self.tree.column("title", width=400)
        self.tree.column("status", width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(self.root, text="批量导出选中文章为.md文件", command=self.on_download_click, bg="#2196F3", fg="white", height=2).pack(fill=tk.X, padx=10, pady=10)

    def select_browser(self):
        file_path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if file_path:
            self.browser_entry.delete(0, tk.END)
            self.browser_entry.insert(0, file_path)

    def on_search_click(self):
        kw = self.kw_entry.get().strip()
        pg = self.pg_entry.get().strip()
        bp = self.browser_entry.get().strip()
        if not kw or not os.path.exists(bp):
            messagebox.showwarning("提示", "请输入关键词并确认浏览器路径是否正确！")
            return
        
        for i in self.tree.get_children(): self.tree.delete(i)
        self.tree.insert("", tk.END, values=("Waiting", "正在加载环境，如有验证请手动处理...", "", "WAITING"))
        
        threading.Thread(target=lambda: self.perform_search(kw, int(pg), bp), daemon=True).start()

    def perform_search(self, kw, pg, bp):
        results = concurrent_search(kw, pg, bp)
        self.root.after(0, lambda: self.update_table(results))

    def update_table(self, data):
        for i in self.tree.get_children(): self.tree.delete(i)
        for item in data:
            self.tree.insert("", tk.END, values=(item["site"], item["title"], item["url"], "就绪"))

    def on_download_click(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请在列表中选择所需要下载的文章")
            return
        
        save_dir = filedialog.askdirectory()
        if not save_dir: return
        browser_path = self.browser_entry.get().strip()
        
        for item_id in selected_items:
            values = self.tree.item(item_id, "values")
            self.tree.set(item_id, "status", "下载中...")
            threading.Thread(target=self.download_task, args=(item_id, values[1], values[2], save_dir, browser_path), daemon=True).start()

    def download_task(self, item_id, title, url, save_dir, bp):
        safe_title = "".join([c for c in title if c.isalnum() or c in " -_"]).strip()
        file_path = os.path.join(save_dir, f"{safe_title}.md")
        success = download_as_md(url, file_path, bp)
        self.root.after(0, lambda: self.tree.set(item_id, "status", "完成" if success else "失败"))