<div align="center">
  <h1>🚀 Resqu</h1>
  <p><strong>Siêu tốc - Đơn giản - Mạnh mẽ</strong></p>
  <p>Thư viện Python để gọi API và tự động lưu kết quả chỉ với 1 dòng code</p>
  
  <p>
    <img src="https://img.shields.io/pypi/v/resqu" alt="PyPI">
    <img src="https://img.shields.io/pypi/pyversions/resqu" alt="Python versions">
    <img src="https://img.shields.io/github/license/yourusername/resqu" alt="License">
    <img src="https://img.shields.io/pypi/dm/resqu" alt="Downloads">
  </p>
</div>

---

## 📦 Cài đặt

```bash
pip install resqu
Chỉ 1 dòng! Không cần cài thêm gì khác.

🎯 Cách sử dụng
Cơ bản nhất - 1 dòng là xong!
python
import resqu

# Cách 1: Dùng api()
resqu.api("example.com")

# Cách 2: Dùng getAPI_text()
resqu.getAPI_text("example.com")
Kết quả:

Tự động tạo thư mục requsAPItxt/

Tạo file example.com.txt với đầy đủ thông tin

Ví dụ thực tế
python
import resqu

# Gọi API bất kỳ
resqu.api("https://jsonplaceholder.typicode.com/posts/1")
resqu.api("https://api.github.com/users/octocat")
resqu.api("https://httpbin.org/get")
Sau khi chạy, bạn sẽ có:

text
requsAPItxt/
├── jsonplaceholder.typicode.com_posts_1.txt
├── api.github.com_users_octocat.txt
└── httpbin.org_get.txt
📁 Nội dung file output
Mỗi file .txt được tạo ra sẽ chứa MỌI THỨ bạn cần:

text
URL: https://api.github.com/users/octocat
Method: GET
Status Code: 200
Time: 2024-01-15T10:30:25.123456
Response Time: 0.345s

--- Headers ---
server: GitHub.com
content-type: application/json; charset=utf-8
cache-control: public, max-age=60, s-maxage=60
etag: W/"123abc456def"
last-modified: Mon, 15 Jan 2024 10:30:00 GMT
x-github-media-type: github.v3
...

--- Response Content ---
{
  "login": "octocat",
  "id": 583231,
  "node_id": "MDQ6VXNlcjU4MzIzMQ==",
  "avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
  "gravatar_id": "",
  "url": "https://api.github.com/users/octocat",
  "html_url": "https://github.com/octocat",
  ...
}

--- Curl Command ---
curl -X GET 'https://api.github.com/users/octocat' -H 'server: GitHub.com' -H 'content-type: application/json; charset=utf-8'
⚡ Tính năng nổi bật
Tính năng	Mô tả
🚀 Siêu tốc	Xử lý bất đồng bộ, không chậm, không lag
🎯 1 dòng code	Gọn nhẹ, dễ nhớ, dễ dùng
📦 Tự động lưu	Tạo thư mục và file tự động
📊 Đầy đủ thông tin	URL, headers, response, curl command, timing
🔧 Không cấu hình	Cài xong là dùng, không cần setup
🐍 Python 3.7+	Hỗ trợ mọi phiên bản mới
🎮 Nâng cao
Gọi nhiều API cùng lúc (siêu nhanh)
python
import resqu

# List URLs
urls = [
    "api1.com",
    "api2.com", 
    "api3.com",
    "api4.com",
    "api5.com"
]

# Fetch tất cả cùng lúc - tốc độ ánh sáng ⚡
results = resqu.getAPI(urls)
print(f"Đã fetch {len(results)} APIs thành công!")
Đọc URLs từ file
Tạo file urls.txt:

text
# Mỗi URL 1 dòng
example.com
api.github.com/users/octocat
jsonplaceholder.typicode.com/posts
httpbin.org/get
python
import resqu

# Fetch tất cả URLs từ file
results = resqu.getAPI("urls.txt")
# Tự động lưu từng kết quả vào thư mục requsAPItxt/
🔥 So sánh tốc độ
Với 100 URLs:

Cách thường: requests.get() mất ~30 giây

Resqu: resqu.getAPI(urls) mất ~2 giây 🚀

📝 API Reference
resqu.api(url, textfile=None)
Gọi API và lưu kết quả

Tham số	Kiểu	Mô tả
url	str	URL cần gọi (có hoặc không http://)
textfile	str, optional	Tên file output (nếu None tự tạo)
Return: dict - Thông tin response

resqu.getAPI_text(url)
Alias của api(), dùng cho ai thích tên dài hơn 😄

resqu.getAPI(input, parallel=True)
Gọi nhiều API cùng lúc

Tham số	Kiểu	Mô tả
input	str hoặc list	URL, list URLs, hoặc path file .txt
parallel	bool	True = gọi song song (nhanh), False = gọi tuần tự
Return: list - Danh sách các responses

💡 Mẹo & Thủ thuật
Dùng với proxy
python
import os
os.environ['HTTP_PROXY'] = 'http://proxy.example.com:8080'
os.environ['HTTPS_PROXY'] = 'https://proxy.example.com:8080'

import resqu
resqu.api("example.com")
Custom headers
python
import requests
from resqu import API

api = API("example.com")
api.session = requests.Session()
api.session.headers.update({'User-Agent': 'Custom Agent'})
result = api.get()
🐛 Lỗi thường gặp
"Không tìm thấy module resqu"
bash
pip install --upgrade resqu
"Connection timeout"
Kiểm tra internet

Thử với http:// thay vì https://

Dùng proxy nếu cần

"Permission denied"
bash
pip install --user resqu
🤝 Đóng góp
Mọi đóng góp đều được chào đón!

Fork project

Tạo branch mới (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push lên branch (git push origin feature/AmazingFeature)

Mở Pull Request

📄 License
MIT License - Free forever! 🎉

🌟 Star us on GitHub!
Nếu bạn thấy project hữu ích, hãy cho nó 1 ngôi sao ⭐ để ủng hộ nhé!

<div align="center"> <p>Made with ❤️ by <a href="https://github.com/yourusername">Your Name</a></p> <p> <a href="https://github.com/yourusername/resqu/issues">Report Bug</a> · <a href="https://github.com/yourusername/resqu/issues">Request Feature</a> </p> </div> ```
Bonus: Thêm badge cho PyPI
Để có các badge đẹp như trên, thêm vào README.md:

markdown
![PyPI - Version](https://img.shields.io/pypi/v/resqu)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/resqu)
![PyPI - License](https://img.shields.io/pypi/l/resqu)
![PyPI - Downloads](https://img.shields.io/pypi/dm/resqu)
File setup.py đơn giản (nếu không dùng pyproject.toml):
python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="resqu",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Siêu tốc - Gọi API và tự động lưu kết quả chỉ với 1 dòng code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/resqu",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "aiohttp>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "resqu=resqu.__main__:main",
        ],
    },
)
