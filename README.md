# Tìm đường đi ngắn nhất trong khuôn viên HUST
Chương trình Python tìm đường đi ngắn nhất giữa các tòa nhà, cổng và địa điểm trong khuôn viên Đại học Bách khoa Hà Nội bằng thuật toán Dijkstra. Hỗ trợ cả giao diện dòng lệnh (CLI) và giao diện web tương tác trên bản đồ thật.

## Tính năng
- Cài đặt thủ công thuật toán Dijkstra với `heapq` (min-heap).
- Biểu diễn đồ thị bằng danh sách kề (adjacency list).
- Tìm kiếm theo mã địa điểm (ví dụ `NORTH_GATE`) hoặc tên hiển thị (ví dụ `Thư viện Tạ Quang Bửu`).
- Giao diện web kiểu Google Maps: click chọn điểm trên bản đồ thật của trường, hiển thị đường đi.
- Vẽ đường đi bằng matplotlib và lưu ra file ảnh.
- Kiểm tra hiệu năng trên cả bản đồ HUST và đồ thị ngẫu nhiên kích thước lớn.

## Cấu trúc dự án
```
hust-campus-shortest-path/
├── main.py                 # Điểm vào CLI
├── map-dhbk.jpg            # Ảnh bản đồ HUST dùng cho giao diện web
├── requirements.txt        # Các thư viện cần cài
├── src/                    # Mã nguồn lõi
│   ├── models.py           # Lớp Vertex, DijkstraResult
│   ├── graph.py            # Cấu trúc đồ thị
│   ├── dijkstra.py         # Thuật toán Dijkstra
│   ├── data_io.py          # Đọc/ghi CSV
│   ├── navigator.py        # Lớp điều phối CampusNavigator
│   ├── performance.py      # Benchmark
│   └── visualize.py        # Vẽ đường đi với matplotlib
├── web/                    # Giao diện web (Flask + Leaflet)
│   ├── app.py              # Backend Flask
│   └── templates/index.html# Frontend Leaflet
├── data/                   # Dữ liệu bản đồ
│   ├── hust_nodes.csv      # Danh sách địa điểm
│   └── hust_edges.csv      # Danh sách lối đi giữa các địa điểm
├── docs/                   # Tài liệu thuật toán và báo cáo
├── tests/                  # Unit test
└── output/                 # Nơi lưu kết quả (ảnh, file txt)
```

## Cài đặt
Yêu cầu Python 3.9 trở lên.

```bash
pip install -r requirements.txt
```

## Sử dụng
### 1. Giao diện web (khuyến nghị)
Khởi động web server:

```bash
python web/app.py
```

Mở trình duyệt tại `http://127.0.0.1:5000` và:

- Click vào một điểm để chọn **điểm bắt đầu** (đổi màu xanh lá).
- Click điểm thứ hai để chọn **điểm kết thúc** (đổi màu đỏ) — đường đi ngắn nhất tự động vẽ trên bản đồ.
- Click vào điểm đã chọn để bỏ chọn; nhấn **Reset** để xóa toàn bộ.
- Bảng bên trái hiển thị tổng khoảng cách, số node trên đường, số node đã duyệt, thời gian chạy và đầy đủ chuỗi đường đi.

### 2. CLI — Liệt kê toàn bộ địa điểm

```bash
python main.py --list
```

### 3. CLI — Tìm đường theo mã

```bash
python main.py --start NORTH_GATE --end TQB_LIBRARY
```

### 4. CLI — Tìm đường theo tên

```bash
python main.py --start "Cổng Bắc" --end "Thư viện Tạ Quang Bửu"
```

### 5. CLI — Vẽ đường đi ra ảnh PNG

```bash
python main.py --start NORTH_GATE --end B1 --visualize
```

Ảnh sẽ được lưu vào `output/hust_shortest_path.png`.

### 6. CLI — Lưu kết quả ra file văn bản

```bash
python main.py --start NORTH_GATE --end B1 --save output/result.txt
```

### 7. CLI — Benchmark trên bản đồ HUST thực tế

```bash
python main.py --test
```

### 8. CLI — Benchmark trên đồ thị ngẫu nhiên

```bash
python main.py --benchmark --nodes 1000 --edges 4000
```

Có thể tùy chỉnh thêm `--seed`, `--runs` để kiểm soát tính lặp lại và số lần chạy.

## Dữ liệu bản đồ

- `data/hust_nodes.csv`: mỗi dòng mô tả một địa điểm với các cột `id, name, type, x, y, description, visible`. Tọa độ `x, y` là vị trí pixel trên ảnh `map-dhbk.jpg` (904×556 px), trục y tăng từ trên xuống dưới. `visible=0` để tạo *đỉnh phụ ẩn* (ví dụ ngã ba, ngã tư) — đỉnh này tham gia vào Dijkstra nhưng không hiện marker trên UI.
- `data/hust_edges.csv`: mỗi dòng mô tả một lối đi với các cột `from, to, weight, bidirectional, waypoints`. `weight` là khoảng cách ước lượng theo mét; `bidirectional=1` nghĩa là đi được hai chiều. `waypoints` (tuỳ chọn) là chuỗi điểm trung gian theo định dạng `"x1,y1;x2,y2;..."` để bẻ cong đường vẽ trên bản đồ theo lối đi thật (cần đặt trong dấu nháy kép vì có dấu phẩy).

Hai cơ chế `visible=0` và `waypoints` có thể dùng kết hợp: dùng đỉnh phụ ẩn cho các ngã rẽ thật sự (nhiều con đường dùng chung), dùng `waypoints` cho các đoạn cong không có nhánh rẽ. Có thể chỉnh sửa hai file CSV để bổ sung địa điểm mới hoặc điều chỉnh sơ đồ kết nối — chương trình sẽ tự động dùng dữ liệu mới ở lần chạy kế tiếp.

## Tài liệu

Thông tin chi tiết về thuật toán và đánh giá hiệu năng nằm trong thư mục `docs/`:

- [Mã giả thuật toán](docs/pseudocode.md)
- [Phân tích độ phức tạp](docs/complexity.md)
- [Giải thích cấu trúc dữ liệu](docs/data_structure_explanation.md)
- [Kết quả kiểm tra hiệu năng](docs/performance_test.md)
- [Báo cáo kỹ thuật đầy đủ](docs/technical_report_vn.md)
