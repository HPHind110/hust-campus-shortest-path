# HUST Campus Shortest Path

Ứng dụng tìm đường đi ngắn nhất trong khuôn viên trường Đại học Bách khoa Hà Nội bằng thuật toán Dijkstra.

## Đặc điểm nổi bật
- Hiện thực thuật toán Dijkstra bằng Python sử dụng `heapq`.
- Thiết kế hướng đối tượng (OOP) với các lớp: Vertex, Edge, Graph, DijkstraResult, CampusNavigator.
- Hỗ trợ tìm kiếm theo ID địa điểm hoặc tên tiếng Việt.
- Dữ liệu bản đồ HUST mô phỏng dựa trên vị trí tương đối.
- Tích hợp công cụ benchmark và trực quan hóa đường đi.

## Hướng dẫn sử dụng

### 1. Liệt kê tất cả địa điểm
```bash
python main.py --list
```

### 2. Tìm đường đi ngắn nhất (bằng ID hoặc Tên)
```bash
python main.py --start NORTH_GATE --end TQB_LIBRARY
```

### 3. Tìm đường và trực quan hóa sơ đồ
```bash
python main.py --start NORTH_GATE --end STADIUM --visualize
```

### 4. Chạy Benchmark hiệu năng
Trên đồ thị HUST:
```bash
python main.py --test
```

Trên đồ thị ngẫu nhiên quy mô lớn:
```bash
python main.py --benchmark --nodes 10000 --edges 40000 --seed 42 --runs 5
```

## Tài liệu chi tiết
- [Báo cáo kỹ thuật (Tiếng Việt)](docs/technical_report_vn.md)
- [Phân tích độ phức tạp](docs/complexity.md)
- [Kết quả kiểm thử hiệu năng](docs/performance_test.md)
