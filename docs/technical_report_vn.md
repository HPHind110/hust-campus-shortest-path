# Báo cáo kỹ thuật: Ứng dụng tìm đường đi ngắn nhất trong khuôn viên HUST bằng thuật toán Dijkstra

## 1. Giới thiệu đề tài

Dự án xây dựng một chương trình mô phỏng chức năng tìm đường đi ngắn nhất giữa các địa điểm trong khuôn viên Đại học Bách khoa Hà Nội (HUST). Bài toán được mô hình hóa bằng đồ thị có trọng số, trong đó mỗi địa điểm là một đỉnh và mỗi lối đi giữa hai địa điểm là một cạnh.

Người dùng có thể chọn điểm bắt đầu và điểm kết thúc thông qua giao diện dòng lệnh. Chương trình sau đó áp dụng thuật toán Dijkstra để tính đường đi có tổng trọng số nhỏ nhất và trả về thông tin kết quả.

Mục tiêu chính của dự án là:

- Áp dụng kiến thức về cấu trúc dữ liệu đồ thị vào một bài toán gần thực tế.
- Hiện thực thuật toán Dijkstra bằng Python.
- Tổ chức dữ liệu bản đồ dưới dạng tệp CSV để dễ chỉnh sửa và mở rộng.
- Đánh giá hiệu năng thuật toán trên cả dữ liệu mô phỏng HUST và đồ thị ngẫu nhiên kích thước lớn.

Dự án không nhằm xây dựng một hệ thống dẫn đường GPS hoàn chỉnh. Dữ liệu bản đồ trong project chỉ mang tính mô phỏng, phục vụ mục tiêu học thuật và minh họa thuật toán.

---

## 2. Phân tích bài toán

### 2.1. Đầu vào

Chương trình nhận các loại dữ liệu đầu vào sau:

- Danh sách địa điểm được đọc từ file `data/hust_nodes.csv`.
- Danh sách lối đi giữa các địa điểm được đọc từ file `data/hust_edges.csv`.
- Điểm bắt đầu và điểm kết thúc do người dùng nhập thông qua tham số dòng lệnh.
- Các tham số benchmark như số lượng node, số lượng cạnh phụ, seed và số lần chạy.

### 2.2. Đầu ra

Sau khi chạy thuật toán, chương trình trả về:

- Tổng khoảng cách ngắn nhất từ điểm bắt đầu đến điểm kết thúc.
- Danh sách các địa điểm nằm trên đường đi ngắn nhất.
- Số lượng đỉnh đã được duyệt trong quá trình chạy thuật toán.
- Thời gian thực thi thuật toán.
- Ảnh trực quan hóa đường đi nếu người dùng bật tùy chọn `--visualize`.

### 2.3. Ràng buộc

Thuật toán Dijkstra chỉ đảm bảo đúng với đồ thị có trọng số không âm. Vì vậy, chương trình cần đảm bảo:

- Trọng số cạnh phải là số không âm.
- Đỉnh bắt đầu và đỉnh kết thúc phải tồn tại trong đồ thị.
- Đồ thị có thể chứa cạnh một chiều hoặc hai chiều, tùy theo dữ liệu đầu vào.
- Dữ liệu bản đồ HUST là dữ liệu mô phỏng, không phải dữ liệu đo đạc địa lý chính thức.

---

## 3. Mô hình hóa bản đồ HUST thành đồ thị

Bản đồ khuôn viên HUST được mô hình hóa thành một đồ thị có trọng số:

- **Đỉnh (Vertex):** Đại diện cho một địa điểm trong khuôn viên, ví dụ như cổng trường, tòa nhà, thư viện, hồ hoặc sân vận động.
- **Cạnh (Edge):** Đại diện cho một lối đi giữa hai địa điểm.
- **Trọng số (Weight):** Đại diện cho khoảng cách ước lượng giữa hai địa điểm.

Một số địa điểm tiêu biểu trong dữ liệu:

- `NORTH_GATE`: Cổng phía Bắc.
- `WEST_GATE`: Cổng phía Tây.
- `EAST_GATE`: Cổng phía Đông.
- `C1`, `C2`, `C3`, ...: Các tòa nhà khu C.
- `TQB_LIBRARY`: Thư viện Tạ Quang Bửu.
- `TIEN_LAKE`: Hồ Tiền.
- `STADIUM`: Sân vận động Bách khoa.

Việc sử dụng mã định danh như `TQB_LIBRARY` giúp chương trình xử lý dữ liệu ổn định hơn so với việc dùng trực tiếp tên tiếng Việt có dấu. Khi hiển thị cho người dùng, chương trình có thể dùng tên đầy đủ như “Thư viện Tạ Quang Bửu”.

Lưu ý: Tọa độ `x, y` trong dữ liệu chỉ dùng để trực quan hóa tương đối trên mặt phẳng 2D. Chúng không phải tọa độ GPS thực tế.

---

## 4. Cấu trúc dữ liệu và thiết kế lớp

Dự án được hiện thực bằng Python theo hướng lập trình hướng đối tượng. Các thành phần chính gồm:

### 4.1. Vertex

`Vertex` biểu diễn một địa điểm trong đồ thị.

Mỗi đỉnh có thể chứa các thông tin:

- `id`: Mã định danh duy nhất của địa điểm.
- `name`: Tên hiển thị của địa điểm.
- `type`: Loại địa điểm.
- `x`, `y`: Tọa độ mô phỏng dùng cho trực quan hóa.
- `description`: Mô tả ngắn về địa điểm.

### 4.2. Edge

`Edge` biểu diễn một cạnh nối giữa hai đỉnh.

Thông tin chính của một cạnh gồm:

- `source`: Đỉnh nguồn.
- `destination`: Đỉnh đích.
- `weight`: Trọng số cạnh.
- `label`: Nhãn hoặc mô tả cạnh nếu có.

### 4.3. Graph

`Graph` quản lý tập đỉnh và tập cạnh của bản đồ.

Đồ thị được lưu bằng **danh sách kề (Adjacency List)**. Cách biểu diễn này phù hợp với bản đồ khuôn viên vì mỗi địa điểm thường chỉ nối với một số lượng nhỏ địa điểm lân cận. So với ma trận kề, danh sách kề tiết kiệm bộ nhớ hơn đối với đồ thị thưa.

Các phương thức chính:

- `addVertex`: Thêm đỉnh vào đồ thị.
- `addEdge`: Thêm cạnh vào đồ thị.
- `getNeighbors`: Lấy danh sách các đỉnh kề của một đỉnh.
- `getVertex`: Lấy thông tin một đỉnh theo ID.
- `getVertexCount`: Trả về số lượng đỉnh.
- `getEdgeCount`: Trả về số lượng cạnh.

### 4.4. DijkstraResult

`DijkstraResult` dùng để đóng gói kết quả trả về từ thuật toán Dijkstra.

Các thông tin chính gồm:

- `source_id`: ID điểm bắt đầu.
- `dest_id`: ID điểm kết thúc.
- `total_distance`: Tổng khoảng cách ngắn nhất.
- `path`: Danh sách các đỉnh trên đường đi.
- `found`: Trạng thái có tìm thấy đường đi hay không.
- `visited_count`: Số lượng đỉnh đã duyệt.
- `elapsed_ms`: Thời gian chạy thuật toán, tính bằng mili-giây.

### 4.5. CampusNavigator

`CampusNavigator` đóng vai trò điều phối chính của ứng dụng.

Lớp này phụ trách:

- Đọc dữ liệu từ file CSV.
- Lưu dữ liệu hoặc kết quả nếu cần.
- Tìm đường đi ngắn nhất giữa hai địa điểm.
- Liệt kê các địa điểm hiện có.
- Chạy kiểm thử hiệu năng.

---

## 5. Đọc và lưu dữ liệu

Dữ liệu được lưu trong thư mục `data`.

### 5.1. File `data/hust_nodes.csv`

File này chứa danh sách các địa điểm trong bản đồ mô phỏng.

Các cột chính:

- `id`
- `name`
- `type`
- `x`
- `y`
- `description`

### 5.2. File `data/hust_edges.csv`

File này chứa danh sách các cạnh nối giữa các địa điểm.

Các cột chính:

- `from`
- `to`
- `weight`
- `bidirectional`

Trong đó, `bidirectional` cho biết cạnh có phải cạnh hai chiều hay không. Nếu cạnh là hai chiều, chương trình sẽ thêm cả chiều ngược lại vào đồ thị.

### 5.3. Quy trình nạp dữ liệu

Khi chương trình khởi động, dữ liệu được đọc từ các file CSV. Sau đó:

1. Tạo các đối tượng `Vertex` từ file node.
2. Thêm các đỉnh vào đồ thị.
3. Đọc các cạnh từ file edge.
4. Thêm cạnh vào danh sách kề.
5. Kiểm tra tính hợp lệ cơ bản của dữ liệu.

Cách tổ chức này giúp dữ liệu bản đồ tách biệt khỏi phần xử lý thuật toán. Vì vậy, khi muốn cập nhật bản đồ, ta chỉ cần chỉnh sửa file CSV mà không cần thay đổi logic chính của chương trình.

---

## 6. Thuật toán Dijkstra

Thuật toán Dijkstra được sử dụng để tìm đường đi ngắn nhất từ một đỉnh nguồn đến một đỉnh đích trong đồ thị có trọng số không âm.

Ý tưởng chính của thuật toán là:

1. Ban đầu, khoảng cách từ điểm bắt đầu đến chính nó bằng 0.
2. Khoảng cách từ điểm bắt đầu đến các đỉnh khác được đặt là vô cùng.
3. Luôn chọn đỉnh chưa xử lý có khoảng cách tạm thời nhỏ nhất.
4. Cập nhật khoảng cách đến các đỉnh kề nếu tìm được đường đi ngắn hơn.
5. Lặp lại quá trình trên cho đến khi tìm được đỉnh đích hoặc không còn đỉnh nào có thể cải thiện.

### 6.1. Các cấu trúc dữ liệu sử dụng

- `distances`: Lưu khoảng cách ngắn nhất hiện biết từ đỉnh bắt đầu đến từng đỉnh.
- `parents`: Lưu đỉnh đứng trước mỗi đỉnh trên đường đi ngắn nhất.
- `priority queue`: Hàng đợi ưu tiên dùng để lấy ra đỉnh có khoảng cách tạm thời nhỏ nhất.
- `visited`: Tập các đỉnh đã được xử lý chắc chắn.

### 6.2. Bước nới lỏng cạnh (Relaxation)

Với mỗi cạnh từ `u` đến `v` có trọng số `w`, nếu:

```text
dist[u] + w < dist[v]
````

thì ta cập nhật:

```text
dist[v] = dist[u] + w
parent[v] = u
```

Đây là bước quan trọng nhất của thuật toán. Nó thể hiện việc tìm được một đường đi tốt hơn đến đỉnh `v` thông qua đỉnh `u`.

### 6.3. Dừng sớm

Trong bài toán này, ta chỉ cần tìm đường đi từ một điểm bắt đầu đến một điểm kết thúc cụ thể. Vì vậy, khi đỉnh đích được lấy ra khỏi hàng đợi ưu tiên, khoảng cách đến nó đã là tối ưu. Thuật toán có thể dừng ngay mà không cần tiếp tục xử lý toàn bộ đồ thị.

### 6.4. Mã giả

```text
Dijkstra(graph, start, target):
    for each vertex v in graph:
        dist[v] = infinity
        parent[v] = None

    dist[start] = 0
    heap = [(0, start)]

    while heap is not empty:
        current_distance, u = pop vertex with smallest distance from heap

        if u has already been visited:
            continue

        mark u as visited

        if u == target:
            break

        for each neighbor v of u with edge weight w:
            new_distance = current_distance + w

            if new_distance < dist[v]:
                dist[v] = new_distance
                parent[v] = u
                push (new_distance, v) into heap

    reconstruct path by tracing parent from target back to start
    return dist[target] and path
```

---

## 7. Độ phức tạp thuật toán

Gọi:

* `V` là số lượng đỉnh.
* `E` là số lượng cạnh.

Với cách cài đặt bằng danh sách kề và hàng đợi ưu tiên dạng Min-Heap:

### 7.1. Độ phức tạp thời gian

```text
O((V + E) log V)
```

Lý do:

* Mỗi đỉnh có thể được đưa vào hoặc lấy ra khỏi heap.
* Mỗi cạnh được xét trong quá trình duyệt danh sách kề.
* Mỗi thao tác cập nhật trong heap có chi phí xấp xỉ `O(log V)`.

### 7.2. Độ phức tạp không gian

```text
O(V + E)
```

Lý do:

* Danh sách kề cần lưu thông tin đỉnh và cạnh.
* Các cấu trúc phụ như `distances`, `parents`, `visited` và `heap` cần bộ nhớ tỷ lệ với số lượng đỉnh.

---

## 8. Chức năng dòng lệnh

Ứng dụng cung cấp giao diện dòng lệnh thông qua file `main.py`.

### 8.1. Liệt kê địa điểm

```bash
python main.py --list
```

Lệnh này hiển thị danh sách các địa điểm có trong dữ liệu.

### 8.2. Tìm đường đi ngắn nhất

```bash
python main.py --start NORTH_GATE --end TQB_LIBRARY
```

Lệnh này tìm đường đi ngắn nhất từ `NORTH_GATE` đến `TQB_LIBRARY`.

### 8.3. Tìm đường và trực quan hóa

```bash
python main.py --start NORTH_GATE --end STADIUM --visualize
```

Lệnh này vừa tìm đường đi ngắn nhất vừa tạo ảnh trực quan hóa đường đi.

### 8.4. Chạy benchmark

```bash
python main.py --benchmark --nodes 10000 --edges 40000 --seed 42 --runs 5
```

Lệnh này sinh một đồ thị ngẫu nhiên có 10.000 đỉnh và 40.000 cạnh phụ, sau đó chạy Dijkstra nhiều lần để đo hiệu năng.

### 8.5. Ý nghĩa các tham số

* `--list`: Hiển thị danh sách địa điểm.
* `--start`: Điểm bắt đầu.
* `--end`: Điểm kết thúc.
* `--visualize`: Bật trực quan hóa đường đi.
* `--benchmark`: Chạy kiểm thử hiệu năng.
* `--nodes`: Số lượng đỉnh trong đồ thị benchmark.
* `--edges`: Số lượng cạnh phụ trong đồ thị benchmark.
* `--seed`: Giá trị seed để sinh đồ thị ngẫu nhiên có thể tái lập.
* `--runs`: Số lần chạy thuật toán trên cùng một đồ thị benchmark.

---

## 9. Trực quan hóa đường đi

Chức năng trực quan hóa sử dụng tọa độ `x, y` của các đỉnh để vẽ sơ đồ đơn giản trên mặt phẳng 2D.

Kết quả trực quan hóa gồm:

* Các đỉnh đại diện cho địa điểm.
* Các cạnh đại diện cho lối đi.
* Đường đi ngắn nhất được làm nổi bật.
* Ảnh kết quả được lưu trong thư mục `output`.

Ví dụ file kết quả:

```text
output/hust_shortest_path.png
```

Cần lưu ý rằng sơ đồ này chỉ nhằm minh họa quan hệ giữa các địa điểm trong dữ liệu mô phỏng. Nó không thay thế cho bản đồ địa lý thực tế.

---

## 10. Benchmark hiệu năng

Để đánh giá khả năng mở rộng của thuật toán, dự án thực hiện benchmark trên các đồ thị ngẫu nhiên có kích thước lớn.

### 10.1. Quy trình sinh đồ thị benchmark

Với một đồ thị có `n` đỉnh, chương trình thực hiện:

1. Tạo các đỉnh có ID từ `0` đến `n - 1`.
2. Tạo một chuỗi cạnh cơ bản:

```text
0 - 1 - 2 - ... - (n - 1)
```

Chuỗi cạnh này đảm bảo đồ thị luôn liên thông.

3. Thêm các cạnh phụ ngẫu nhiên giữa các cặp đỉnh khác nhau.
4. Gán trọng số ngẫu nhiên không âm cho các cạnh.
5. Chạy Dijkstra từ đỉnh `0` đến đỉnh `n - 1`.
6. Lặp lại thuật toán nhiều lần trên cùng một đồ thị để thu thập thống kê thời gian chạy.

### 10.2. Tính tái lập của benchmark

Tham số `seed` giúp quá trình sinh đồ thị ngẫu nhiên có thể tái lập. Khi dùng cùng một số node, số cạnh phụ, trọng số tối đa và seed, cấu trúc đồ thị được sinh ra sẽ giống nhau.

Tuy nhiên, thời gian chạy `elapsed_ms` không thể giống tuyệt đối giữa các lần chạy. Nguyên nhân là thời gian thực thi phụ thuộc vào nhiều yếu tố của hệ thống như CPU scheduling, cache, tiến trình nền và trạng thái máy tại thời điểm chạy.

Vì vậy, benchmark không nên chỉ nhìn vào một lần chạy đơn lẻ. Thay vào đó, chương trình báo cáo các chỉ số thống kê như:

* Thời gian trung bình.
* Trung vị.
* Thời gian nhỏ nhất.
* Thời gian lớn nhất.

### 10.3. Kết quả benchmark tham khảo

| Số node | Cạnh phụ yêu cầu | Cạnh phụ thêm được | Tổng số cạnh | Seed | Số lần chạy | Avg runtime (ms) | Median runtime (ms) | Min-Max runtime (ms) |
| ------: | ---------------: | -----------------: | -----------: | ---: | ----------: | ---------------: | ------------------: | -------------------: |
|   1.000 |            4.000 |              4.000 |        4.999 |   42 |           5 |           2.5499 |              2.5199 |      2.4970 - 2.6903 |
|   5.000 |           20.000 |             20.000 |       24.999 |   42 |           5 |          16.4899 |             16.1804 |    14.9043 - 18.6098 |
|  10.000 |           40.000 |             40.000 |       49.999 |   42 |           5 |          37.8451 |             38.2507 |    33.5482 - 42.3584 |

### 10.4. Nhận xét

Kết quả cho thấy thuật toán Dijkstra khi kết hợp với danh sách kề và Min-Heap có thể xử lý tốt các đồ thị thưa kích thước lớn.

Với đồ thị 10.000 đỉnh và khoảng 50.000 cạnh, thời gian chạy trung bình vẫn ở mức vài chục mili-giây trên môi trường thử nghiệm. Điều này phù hợp với kỳ vọng lý thuyết của thuật toán trên đồ thị thưa.

Tuy nhiên, các số liệu benchmark chỉ có ý nghĩa tham khảo. Chúng có thể thay đổi tùy theo cấu hình máy, trạng thái hệ thống, phiên bản Python và cách cài đặt chi tiết của chương trình.

---

## 11. Kiểm thử

Dự án kiểm thử các trường hợp chính sau:

### 11.1. Đường đi thông thường

Kiểm tra thuật toán với các cặp điểm có đường đi hợp lệ trong đồ thị. Kết quả cần trả về đúng tổng khoảng cách và đúng thứ tự các đỉnh trên đường đi.

### 11.2. Điểm bắt đầu trùng điểm kết thúc

Nếu điểm bắt đầu và điểm kết thúc giống nhau, khoảng cách ngắn nhất phải bằng 0 và đường đi chỉ gồm một đỉnh.

### 11.3. Điểm không tồn tại

Nếu người dùng nhập ID địa điểm không tồn tại, chương trình cần thông báo lỗi rõ ràng thay vì chạy thuật toán trên dữ liệu không hợp lệ.

### 11.4. Trọng số âm

Vì Dijkstra không áp dụng cho cạnh có trọng số âm, chương trình cần từ chối hoặc cảnh báo khi dữ liệu chứa trọng số âm.

### 11.5. Kiểm thử dòng lệnh

Các lệnh CLI như `--list`, `--start`, `--end`, `--visualize` và `--benchmark` cần hoạt động ổn định sau mỗi lần cập nhật mã nguồn.

---

## 12. Hạn chế của dự án

Dự án hiện tại vẫn còn một số hạn chế:

* Dữ liệu bản đồ HUST là dữ liệu mô phỏng, không phải dữ liệu GPS chính thức.
* Khoảng cách giữa các địa điểm chỉ là ước lượng.
* Chức năng trực quan hóa còn đơn giản.
* Chưa xét đến các yếu tố thực tế như đường đang thi công, khu vực bị chặn, nhiều lối vào trong cùng một tòa nhà, cầu thang hoặc thang máy.
* Chưa hỗ trợ nhiều tiêu chí tìm đường như thời gian di chuyển, độ thuận tiện hoặc mức độ dễ tiếp cận.
* Giao diện hiện tại là CLI, chưa thân thiện với người dùng phổ thông như web app hoặc mobile app.

---

## 13. Hướng phát triển

Một số hướng có thể mở rộng trong tương lai:

* Tích hợp dữ liệu bản đồ thực tế từ OpenStreetMap hoặc nguồn GPS đáng tin cậy.
* Xây dựng giao diện web để người dùng chọn điểm trực tiếp trên bản đồ.
* Áp dụng thuật toán A* với heuristic dựa trên tọa độ để tăng tốc tìm kiếm.
* Hỗ trợ tìm đường theo nhiều tiêu chí khác nhau.
* Bổ sung hướng dẫn từng bước cho người dùng.
* Cho phép cập nhật trạng thái đường đi theo thời gian thực.
* Cải thiện trực quan hóa bằng thư viện bản đồ chuyên dụng.

---

## 14. Kết luận

Dự án đã hiện thực thành công một ứng dụng tìm đường đi ngắn nhất trong khuôn viên HUST ở mức mô phỏng. Bài toán được mô hình hóa bằng đồ thị có trọng số, dữ liệu được tổ chức bằng file CSV, và thuật toán Dijkstra được sử dụng để tính đường đi ngắn nhất.

Việc sử dụng danh sách kề kết hợp với hàng đợi ưu tiên giúp chương trình đạt hiệu năng tốt trên đồ thị thưa. Kết quả benchmark cho thấy chương trình có khả năng xử lý các đồ thị ngẫu nhiên kích thước lớn trong thời gian hợp lý.
