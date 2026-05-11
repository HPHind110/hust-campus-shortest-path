# Báo cáo kỹ thuật: Ứng dụng tìm đường đi ngắn nhất trong khuôn viên HUST bằng thuật toán Dijkstra

## 1. Giới thiệu đề tài
Dự án tập trung vào việc mô phỏng hệ thống tìm đường đi ngắn nhất bên trong khuôn viên trường Đại học Bách khoa Hà Nội (HUST). 
- Người dùng có thể chọn điểm bắt đầu và điểm kết thúc từ danh sách các địa điểm có sẵn.
- Chương trình tính toán và trả về đường đi ngắn nhất cùng với tổng khoảng cách di chuyển.
- Dự án tập trung vào việc mô hình hóa đồ thị và thuật toán Dijkstra, không phải là một hệ thống dẫn đường GPS chuyên dụng.

## 2. Phân tích bài toán
- **Đầu vào (Input):**
    - Danh sách các địa điểm từ `data/hust_nodes.csv`.
    - Danh sách các con đường từ `data/hust_edges.csv`.
    - Điểm xuất phát và điểm đích từ dòng lệnh.
- **Đầu ra (Output):**
    - Tổng khoảng cách ngắn nhất.
    - Danh sách các điểm đi qua theo thứ tự.
    - Số lượng node đã duyệt.
    - Thời gian thực thi thuật toán.
    - Hình ảnh trực quan hóa sơ đồ đường đi (tùy chọn).
- **Ràng buộc (Constraints):**
    - Trọng số các cạnh phải là số dương hoặc không âm.
    - Đồ thị có thể là vô hướng khi `bidirectional = 1`.
    - Dữ liệu bản đồ HUST mô phỏng dựa trên vị trí tương đối, không phải dữ liệu GPS hoặc số liệu đo đạc chính thức.

## 3. Mô hình hóa bản đồ HUST thành đồ thị
- Mỗi địa điểm trong khuôn viên trường là một **đỉnh (Vertex)**.
- Mỗi lối đi bộ nối giữa hai địa điểm là một **cạnh (Edge)**.
- Mỗi cạnh có trọng số đại diện cho khoảng cách đi bộ xấp xỉ (**Weight**).
- Ví dụ: `NORTH_GATE`, `WEST_GATE`, `EAST_GATE` là các cổng; `C1`, `C2` là các tòa nhà; `TQB_LIBRARY` là Thư viện Tạ Quang Bửu.

## 4. Cấu trúc dữ liệu và Thiết kế lớp
Dự án được hiện thực hóa bằng ngôn ngữ **Python**, tuân thủ thiết kế hướng đối tượng (OOP) theo yêu cầu:

### Tương quan giữa C++ và Python
| Khái niệm C++ / STL | Tương đương trong Python | Vai trò trong Project |
| :--- | :--- | :--- |
| `std::unordered_map` | `dict` | Lưu trữ danh sách đỉnh và danh sách kề |
| `std::vector` | `list` | Lưu trữ đường đi và danh sách lân cận |
| `std::priority_queue`| `heapq` (Min-Heap) | Hàng đợi ưu tiên cho Dijkstra |
| `vertices.txt` | `hust_nodes.csv` | Dữ liệu các địa điểm |
| `edges.txt` | `hust_edges.csv` | Dữ liệu các đoạn đường |

### Các lớp chính
- **Vertex:** Lưu trữ thông tin định danh, tên, tọa độ và mô tả.
- **Edge:** Đại diện cho kết nối giữa nguồn và đích với trọng số xác định.
- **Graph:** Lưu trữ danh sách đỉnh, danh sách kề, tổng số đỉnh và số cạnh. Hỗ trợ các phương thức `addVertex`, `addEdge`, `getNeighbors`, v.v.
- **DijkstraResult:** Bao đóng kết quả tìm kiếm (khoảng cách, đường đi, thời gian, số node đã duyệt).
- **CampusNavigator:** Lớp điều phối trung tâm quản lý dữ liệu và thực hiện các chức năng tìm đường, benchmark.

## 5. Đọc và lưu dữ liệu
- `loadData()`: Đọc các file CSV và xây dựng đồ thị.
- `saveData()`: Ghi kết quả tìm đường ra file text.
- Các cột quan trọng: `id`, `name`, `type`, `x`, `y`, `from`, `to`, `weight`, `bidirectional`.

## 6. Thuật toán Dijkstra
Thuật toán tìm đường đi ngắn nhất từ một nguồn duy nhất đến các đỉnh khác trong đồ thị trọng số không âm.
- **dist:** Khoảng cách ngắn nhất được biết từ nguồn đến mỗi node.
- **parent:** Node trước đó dùng để phục hồi đường đi.
- **heapq/min-heap:** Luôn chọn node có khoảng cách tạm thời nhỏ nhất để tối ưu thời gian tìm kiếm.
- **Relaxation (Thư giãn):** Nếu `dist[u] + weight(u, v) < dist[v]`, cập nhật `dist[v]` và `parent[v]`.
- **Dừng sớm:** Thuật toán dừng ngay khi node đích được lấy ra khỏi Priority Queue.
- **Phục hồi đường đi:** Truy ngược từ đích về nguồn thông qua mảng `parent`.

## 7. Độ phức tạp thuật toán
- **Thời gian:** $O((V + E) \log V)$ nhờ sử dụng Danh sách kề và Min-Heap.
- **Không gian:** $O(V + E)$ để lưu trữ cấu trúc đồ thị và các mảng bổ trợ.

## 8. Chức năng dòng lệnh
- Liệt kê địa điểm: `python main.py --list`
- Tìm đường đi ngắn nhất: `python main.py --start NORTH_GATE --end TQB_LIBRARY`
- Tìm đường và trực quan hóa: `python main.py --start NORTH_GATE --end STADIUM --visualize`
- Benchmark: `python main.py --benchmark --nodes 10000 --edges 40000 --seed 42 --runs 5`

## 9. Trực quan hóa đường đi
Sử dụng tọa độ `x, y` từ dữ liệu mô phỏng để vẽ sơ đồ 2D. Đường đi ngắn nhất được làm nổi bật và lưu vào `output/hust_shortest_path.png`.

## 10. Performance test với dữ liệu lớn
Benchmark sử dụng đồ thị liên thông sinh ngẫu nhiên để kiểm tra khả năng mở rộng.

| Số node | Cạnh phụ yêu cầu | Cạnh phụ thêm được | Tổng số cạnh | Seed | Số lần chạy | Avg runtime (ms) | Median runtime (ms) | Min-Max runtime (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.000 | 4.000 | 4.000 | 4.999 | 42 | 5 | 2.5499 | 2.5199 | 2.4970 - 2.6903 |
| 5.000 | 20.000 | 20.000 | 24.999 | 42 | 5 | 16.4899 | 16.1804 | 14.9043 - 18.6098 |
| 10.000 | 40.000 | 40.000 | 49.999 | 42 | 5 | 37.5876 | 37.7514 | 34.7941 - 40.6592 |

## 11. Kiểm thử
Dự án thực hiện kiểm thử trên các kịch bản: đường đi bình thường, điểm đầu trùng điểm cuối, điểm không tồn tại, và từ chối trọng số âm.

## 12. Hạn chế và Hướng phát triển
- Hạn chế: Dữ liệu mô phỏng, trực quan hóa 2D đơn giản, chỉ hỗ trợ CLI.
- Phát triển: Tích hợp GPS thực, giao diện GUI/Web, thuật toán A*.

## 13. Kết luận
Dự án đã hiện thực hóa thành công mô hình tìm đường đi ngắn nhất với cấu trúc dữ liệu tối ưu và thuật toán Dijkstra hiệu quả, đáp ứng tốt các yêu cầu về hiệu năng và thiết kế hệ thống.
