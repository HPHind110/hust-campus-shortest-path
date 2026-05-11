# Phân tích Độ phức tạp (Complexity Analysis)

Phân tích hiệu năng của thuật toán Dijkstra được hiện thực hóa trong dự án tìm đường HUST.

## 1. Độ phức tạp thời gian (Time Complexity)

Hiện thực sử dụng **Danh sách kề (Adjacency List)** và **Hàng đợi ưu tiên (Min-Heap)** thông qua thư viện `heapq` trong Python.

- **Khởi tạo**: $O(V)$ để thiết lập các khoảng cách ban đầu.
- **Vòng lặp chính**: Thực hiện tối đa $V$ lần.
- **Thao tác Heap**: Mỗi đỉnh được thêm và lấy ra khỏi heap một lần, mỗi cạnh có thể kích hoạt một thao tác `heappush`.
- **Tổng quát**: **$O((V + E) \log V)$**

Trong đó $V$ là số đỉnh và $E$ là số cạnh. Với dữ liệu bản đồ HUST mô phỏng (đồ thị thưa), hiệu năng này là tối ưu.

## 2. Độ phức tạp không gian (Space Complexity)

- **Danh sách kề**: $O(V + E)$
- **Bản đồ khoảng cách/đỉnh cha**: $O(V)$
- **Hàng đợi ưu tiên**: $O(V)$
- **Tổng quát**: **$O(V + E)$**

## 3. Lựa chọn Cấu trúc dữ liệu (Python)

| Thành phần | Lựa chọn | Lý do |
| :--- | :--- | :--- |
| Đồ thị | `dict` (Adjacency List) | Tiết kiệm bộ nhớ cho đồ thị thưa, truy cập lân cận $O(1)$. |
| Priority Queue | `heapq` | Cung cấp các thao tác $O(\log V)$ cho việc lấy đỉnh có khoảng cách nhỏ nhất. |
| Kết quả | `DijkstraResult` class | Bao đóng dữ liệu giúp quản lý và hiển thị thông tin rõ ràng. |

Kiểm chứng thực tế về độ phức tạp này có thể xem tại [Báo cáo Hiệu năng](performance_test.md).
