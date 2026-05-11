# Báo cáo kỹ thuật: Ứng dụng tìm đường đi ngắn nhất trong khuôn viên HUST bằng thuật toán Dijkstra

## 1. Giới thiệu đề tài
Dự án tập trung vào việc mô phỏng hệ thống tìm đường đi ngắn nhất bên trong khuôn viên trường Đại học Bách khoa Hà Nội (HUST). 
- Người dùng có thể chọn điểm bắt đầu và điểm kết thúc từ danh sách các địa điểm có sẵn.
- Chương trình tính toán và trả về đường đi ngắn nhất cùng với tổng khoảng cách di chuyển.
- Mục tiêu chính của dự án là áp dụng kiến thức về cấu trúc dữ liệu đồ thị và thuật toán Dijkstra vào bài toán thực tế, không phải là một hệ thống dẫn đường GPS chuyên dụng.

## 2. Phân tích bài toán
- **Đầu vào (Input):**
    - Danh sách các địa điểm (node) được đọc từ file `data/hust_nodes.csv`.
    - Danh sách các con đường/lối đi (edge) được đọc từ file `data/hust_edges.csv`.
    - Điểm xuất phát và điểm đích do người dùng nhập từ dòng lệnh.
- **Đầu ra (Output):**
    - Tổng khoảng cách ngắn nhất.
    - Danh sách các điểm đi qua theo thứ tự.
    - Số lượng node đã duyệt (visited nodes) để đánh giá hiệu năng.
    - Thời gian thực thi thuật toán.
    - Hình ảnh trực quan hóa sơ đồ đường đi (tùy chọn).
- **Ràng buộc (Constraints):**
    - Trọng số các cạnh (khoảng cách) phải là số dương hoặc không âm.
    - Đồ thị hỗ trợ cả cạnh một chiều và hai chiều (thông qua thuộc tính `bidirectional`).
    - Dữ liệu bản đồ HUST trong project này mang tính chất mô phỏng, dùng để minh họa cho thuật toán.

## 3. Mô hình hóa bản đồ HUST thành đồ thị
Bài toán tìm đường được mô hình hóa thành một đồ thị có trọng số:
- **Đỉnh (Vertex/Node):** Mỗi địa điểm trong khuôn viên trường (cổng, nhà học, thư viện, hồ, sân vận động) là một đỉnh.
- **Cạnh (Edge):** Mỗi lối đi bộ nối giữa hai địa điểm là một cạnh.
- **Trọng số (Weight):** Đại diện cho khoảng cách di chuyển xấp xỉ giữa các địa điểm.
- **Các địa điểm tiêu biểu:**
    - `NORTH_GATE`, `WEST_GATE`, `EAST_GATE`: Các cổng chính của trường.
    - `C1`, `C2`, `C3`, ...: Các tòa nhà học khu C.
    - `TQB_LIBRARY`: Tên định danh (ID) của Thư viện Tạ Quang Bửu. Trong các báo cáo và hiển thị, địa điểm này được trình bày đầy đủ là "Thư viện Tạ Quang Bửu".
    - `TIEN_LAKE`: Hồ Tiền.
    - `STADIUM`: Sân vận động Bách khoa.

*Lưu ý: Dữ liệu bản đồ HUST trong dự án này được mô phỏng dựa trên các vị trí tương đối, không phải là dữ liệu trắc địa hoặc tọa độ GPS chính thức từ cơ quan quản lý.*

## 4. Cấu trúc dữ liệu và Thiết kế lớp
Project được hiện thực hóa bằng ngôn ngữ **Python**, áp dụng thiết kế hướng đối tượng để mô hình hóa bài toán một cách chặt chẽ:

- **Vertex (Đỉnh):** Lưu trữ thông tin định danh, tên, loại địa điểm, tọa độ x-y và mô tả. Thay thế cho khái niệm "Node" trước đây.
- **Edge (Cạnh):** Lưu trữ thông tin đỉnh nguồn (`source`), đỉnh đích (`destination`), trọng số (`weight`) và nhãn (`label`).
- **Graph (Đồ thị):** Quản lý danh sách các đỉnh và danh sách kề. Hỗ trợ các phương thức:
    - `addVertex`, `addEdge`
    - `getNeighbors`, `getVertex`
    - `getVertexCount`, `getEdgeCount`
    - Được biểu diễn bằng **Danh sách kề (Adjacency List)** để tối ưu bộ nhớ.
- **DijkstraResult:** Lớp bao đóng kết quả trả về từ thuật toán Dijkstra, bao gồm:
    - `source_id`, `dest_id`
    - `total_distance`, `path`
    - `found` (trạng thái tìm thấy), `visited_count`
    - `elapsed_ms`
    - Phương thức `print_path()` để hiển thị kết quả một cách chuyên nghiệp.
- **CampusNavigator:** Lớp điều hướng trung tâm, đóng vai trò là bộ não của ứng dụng, quản lý:
    - `loadData`, `saveData`
    - `findShortestPath`
    - `listLocations`
    - `performanceTest`

## 5. Đọc và lưu dữ liệu
- `data/hust_nodes.csv`: Chứa thông tin về các đỉnh với các cột: `id`, `name`, `type`, `x`, `y`, `description`.
- `data/hust_edges.csv`: Chứa thông tin về các cạnh với các cột: `from`, `to`, `weight`, `bidirectional`.
- **Hàm load_data():** Sử dụng thư viện `csv` để đọc dữ liệu từ tệp và xây dựng đồ thị trong bộ nhớ.
- **Hàm save_data():** Hỗ trợ ghi kết quả tìm kiếm ra tệp để lưu trữ báo cáo.

## 6. Thuật toán Dijkstra
Thuật toán Dijkstra được sử dụng để tìm đường đi ngắn nhất từ một đỉnh nguồn đến các đỉnh khác trong đồ thị có trọng số không âm. 
- **Các cấu trúc chính:**
    - `distances`: Lưu khoảng cách ngắn nhất hiện tại từ điểm bắt đầu đến mỗi node.
    - `parents`: Lưu node trước đó của mỗi node để phục hồi lại đường đi.
    - `priority queue (Min-Heap)`: Luôn chọn node có khoảng cách tạm thời nhỏ nhất để duyệt tiếp.
- **Bước thư giãn (Relaxation):** Nếu phát hiện đường đi qua $u$ đến $v$ ngắn hơn đường đi hiện tại đến $v$ ($dist[u] + weight(u, v) < dist[v]$), ta cập nhật lại $dist[v]$ và $parent[v]$.
- **Dừng sớm (Early Stopping):** Khi node đích được lấy ra khỏi Priority Queue, ta chắc chắn đã tìm được đường đi ngắn nhất đến đích và có thể dừng thuật toán ngay lập tức.
- **Phục hồi đường đi:** Sử dụng mảng `parents` để truy ngược từ node đích về node bắt đầu.

### Mã giả thuật toán (Pseudocode):
```text
Dijkstra(graph, start, target):
    dist[start] = 0
    parent[start] = None
    heap = [(0, start)]  # Priority Queue chứa (distance, node_id)

    while heap is not empty:
        current_distance, u = pop node with smallest distance from heap

        if u == target:
            break

        if current_distance > dist[u]:
            continue

        for each neighbor v of u with weight w:
            new_distance = current_distance + w

            if new_distance < dist[v]:
                dist[v] = new_distance
                parent[v] = u
                push (new_distance, v) into heap

    reconstruct path from parent by backtracking from target
    return distance and path
```

## 7. Độ phức tạp thuật toán
Gọi $V$ là số lượng đỉnh và $E$ là số lượng cạnh.
- **Độ phức tạp thời gian:** $O((V + E) \log V)$
    - Do sử dụng Danh sách kề và Priority Queue (Binary Heap).
    - Mỗi cạnh được xét tối đa 2 lần (trong đồ thị vô hướng).
    - Thao tác trên Heap mất $O(\log V)$.
- **Độ phức tạp không gian:** $O(V + E)$
    - Danh sách kề lưu trữ đỉnh và cạnh.
    - Các cấu trúc hỗ trợ như `distances`, `parents` và `heap` đều có kích thước tối đa là $V$.

## 8. Chức năng dòng lệnh
Ứng dụng cung cấp giao diện dòng lệnh (CLI) linh hoạt thông qua tệp `main.py`:

- **Liệt kê địa điểm:**
  `python main.py --list`
- **Tìm đường đi ngắn nhất (theo ID):**
  `python main.py --start NORTH_GATE --end TQB_LIBRARY`
- **Tìm đường và trực quan hóa:**
  `python main.py --start NORTH_GATE --end STADIUM --visualize`
- **Chạy benchmark hiệu năng:**
  `python main.py --benchmark --nodes 10000 --edges 40000 --seed 42 --runs 5`

**Giải thích các tùy chọn:**
- `--list`: Hiển thị danh sách các địa điểm theo nhóm.
- `--start` / `--end`: ID hoặc tên địa điểm bắt đầu và kết thúc.
- `--visualize`: Tạo hình ảnh sơ đồ đường đi.
- `--benchmark`: Chạy kiểm thử hiệu năng trên đồ thị ngẫu nhiên.
- `--nodes` / `--edges`: Số lượng đỉnh và cạnh phụ cho benchmark.
- `--seed`: Hạt giống ngẫu nhiên để đảm bảo kết quả benchmark có thể tái lập.
- `--runs`: Số lần lặp lại benchmark để lấy số liệu thống kê.

## 9. Trực quan hóa đường đi
- Chương trình sử dụng tọa độ `x, y` từ dữ liệu node để vẽ sơ đồ.
- Các đỉnh và cạnh được vẽ trên một mặt phẳng 2D mô phỏng.
- Đường đi ngắn nhất được làm nổi bật để dễ dàng theo dõi.
- Hình ảnh kết quả được lưu tại `output/hust_shortest_path.png`.
- *Lưu ý: Đây chỉ là sơ đồ trực quan hóa đơn giản, không thay thế cho bản đồ địa lý thực tế.*

## 10. Performance test với dữ liệu lớn
Để đánh giá khả năng xử lý của thuật toán, project thực hiện benchmark trên các đồ thị liên thông được sinh ngẫu nhiên với kích thước lớn.

**Quy trình sinh đồ thị benchmark:**
1. Tạo $n$ đỉnh từ 0 đến $n-1$.
2. Tạo một chuỗi liên kết cơ bản (Base edges): $0-1-2-...-(n-1)$. Việc này đảm bảo đồ thị luôn liên thông và luôn có đường đi giữa hai điểm bất kỳ.
3. Thêm các cạnh phụ (Extra edges) ngẫu nhiên giữa các đỉnh dựa trên tham số `--edges`.
4. Thực hiện tìm đường từ đỉnh 0 đến đỉnh cuối cùng $n-1$.
5. Đo lường các chỉ số thời gian thực thi qua nhiều lần chạy.

**Kết quả Benchmark thực tế:**

| Số node | Cạnh phụ yêu cầu | Cạnh phụ thêm được | Tổng số cạnh | Seed | Số lần chạy | Avg runtime (ms) | Median runtime (ms) | Min-Max runtime (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.000 | 4.000 | 4.000 | 4.999 | 42 | 5 | 2.5499 | 2.5199 | 2.4970 - 2.6903 |
| 5.000 | 20.000 | 20.000 | 24.999 | 42 | 5 | 16.4899 | 16.1804 | 14.9043 - 18.6098 |
| 10.000 | 40.000 | 40.000 | 49.999 | 42 | 5 | 37.5876 | 37.7514 | 34.7941 - 40.6592 |

**Nhận xét:**
- Kết quả cho thấy thuật toán Dijkstra với Min-Heap xử lý rất hiệu quả trên các đồ thị thưa. Ngay cả với 10.000 node và 50.000 cạnh, thời gian phản hồi vẫn duy trì ở mức dưới 40ms.
- Việc sử dụng `Median runtime` giúp đánh giá hiệu năng chính xác hơn nhờ loại bỏ các biến động bất thường từ hệ thống.
- Các chỉ số trên đồ thị ngẫu nhiên không đại diện cho bản đồ HUST thực tế nhưng chứng minh được tính ổn định và khả năng mở rộng của mã nguồn.

## 11. Kiểm thử
Dự án bao gồm các trường hợp kiểm thử (test cases) sau:
- **Đường đi thông thường:** Kiểm tra tính đúng đắn trên các cặp điểm có đường đi rõ ràng.
- **Điểm đầu trùng điểm cuối:** Khoảng cách phải bằng 0 và đường đi chỉ chứa một đỉnh.
- **Điểm không tồn tại:** Hệ thống phải thông báo lỗi khi ID địa điểm không hợp lệ.
- **Dữ liệu trọng số âm:** Đồ thị từ chối thêm cạnh có trọng số âm để đảm bảo tính đúng đắn của Dijkstra.
- **Kiểm thử hồi quy CLI:** Đảm bảo các lệnh `--list`, `--start`, `--benchmark` hoạt động ổn định sau mỗi lần cập nhật.

## 12. Hạn chế của dự án
- Dữ liệu bản đồ HUST chỉ mang tính chất mô phỏng, khoảng cách giữa các điểm là ước tính.
- Trực quan hóa bản đồ còn đơn giản, chỉ là sơ đồ 2D phẳng.
- Chưa tính đến các yếu tố thực tế như: đường đang thi công, các tòa nhà có nhiều lối vào, hoặc độ cao (cầu thang).
- Hiện tại chỉ hỗ trợ giao diện dòng lệnh (CLI), chưa có giao diện đồ họa (GUI) cho người dùng phổ thông.

## 13. Hướng phát triển
- Tích hợp dữ liệu thực tế từ OpenStreetMap hoặc GPS.
- Xây dựng giao diện Web hoặc Ứng dụng di động để tăng tính tương tác.
- Áp dụng thuật toán A* với hàm Heuristic dựa trên tọa độ để tăng tốc độ tìm kiếm.
- Hỗ trợ tìm đường theo nhiều tiêu chí: quãng đường ngắn nhất, thời gian di chuyển nhanh nhất, hoặc đường đi thuận tiện nhất cho người khuyết tật.
- Hiển thị hướng dẫn chỉ đường chi tiết từng bước (Step-by-step instructions).

## 14. Kết luận
Dự án đã xây dựng thành công ứng dụng tìm đường đi ngắn nhất trong khuôn viên HUST bằng thuật toán Dijkstra. Thông qua việc sử dụng Danh sách kề và Priority Queue, ứng dụng đạt hiệu năng cao và khả năng mở rộng tốt. Việc tổ chức dữ liệu qua các tệp CSV giúp hệ thống dễ dàng cập nhật và bảo trì. Kết quả benchmark thực tế đã khẳng định tính đúng đắn và hiệu quả của các lựa chọn cấu trúc dữ liệu và thuật toán trong đề tài này.
