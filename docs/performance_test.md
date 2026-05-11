# Báo cáo Kiểm thử Hiệu năng (Performance Test Report)

## Mục tiêu của Benchmark
Quá trình benchmark đánh giá khả năng mở rộng và hiệu quả của thuật toán Dijkstra khi xử lý các đồ thị lớn được sinh ngẫu nhiên. Điều này giúp đảm bảo hệ thống có thể hoạt động ổn định khi khối lượng dữ liệu tăng lên mà không bị suy giảm hiệu năng quá mức.

## Giải thích về Đồ thị Benchmark
Benchmark không sử dụng bản đồ HUST thực tế mà sử dụng các đồ thị liên thông được sinh ngẫu nhiên:
1. **Tính liên thông**: Để đảm bảo luôn tồn tại đường đi, trình sinh đồ thị trước tiên tạo ra một chuỗi (chain) nối từ node 0 đến node n-1 (0-1-2-...-n-1) với n-1 cạnh ban đầu.
2. **Cạnh phụ (Extra edges)**: Sau đó, các "cạnh phụ" được thêm vào giữa các cặp node ngẫu nhiên để tăng độ phức tạp và mật độ của đồ thị.
3. **Trọng số**: Mỗi cạnh được gán một trọng số nguyên dương ngẫu nhiên (mặc định từ 1 đến 100).
4. **Tính hai chiều**: Tất cả các cạnh được coi là cạnh vô hướng (hai chiều).

## Các thông số đo lường
- **Number of nodes**: Tổng số đỉnh của đồ thị.
- **Total edges**: Tổng số cạnh thực tế trong đồ thị (bao gồm n-1 cạnh đảm bảo liên thông và các cạnh phụ).
- **Extra edges requested**: Số lượng cạnh phụ người dùng yêu cầu thêm vào.
- **Extra edges added**: Số lượng cạnh phụ thực tế được thêm vào (có thể ít hơn yêu cầu nếu đồ thị đã quá dày).
- **Seed**: Giá trị hạt giống để đảm bảo đồ thị được sinh ra là như nhau giữa các lần chạy (tính ổn định).
- **Runs**: Số lần chạy thuật toán trên cùng một đồ thị để lấy giá trị thống kê.
- **Avg runtime**: Thời gian chạy trung bình.
- **Median runtime**: Thời gian chạy trung vị. Đây là giá trị quan trọng vì nó ít bị ảnh hưởng bởi các giá trị ngoại lai (outliers) do hệ điều hành hoặc tài nguyên phần cứng tạm thời bận.
- **Min/Max runtime**: Thời gian chạy nhỏ nhất và lớn nhất ghi nhận được.

## Kết quả Benchmark Chi tiết

| Số node | Cạnh phụ yêu cầu | Tổng số cạnh | Seed | Số lần chạy | Avg runtime (ms) | Median runtime (ms) | Min-Max runtime (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.000 | 4.000 | 4.999 | 42 | 5 | 2.5499 | 2.5199 | 2.4970 - 2.6903 |
| 5.000 | 20.000 | 24.999 | 42 | 5 | 16.4899 | 16.1804 | 14.9043 - 18.6098 |
| 10.000 | 40.000 | 49.999 | 42 | 5 | 37.5876 | 37.7514 | 34.7941 - 40.6592 |

## Đánh giá hiệu năng
- **Tính ổn định**: Thời gian chạy (Median) tăng trưởng theo tỉ lệ thuận với $O((V+E) \log V)$, phù hợp với lý thuyết về độ phức tạp của thuật toán Dijkstra sử dụng Min-Heap.
- **Khả năng đáp ứng**: Với 10.000 node và 50.000 cạnh, thuật toán vẫn hoàn thành trong dưới 40ms, mức thời gian lý tưởng cho các ứng dụng tìm đường thực tế.

## Hiệu năng trên bản đồ HUST
Ngoài benchmark trên đồ thị ngẫu nhiên, hệ thống cũng hỗ trợ kiểm thử trực tiếp trên dữ liệu HUST map thông qua lệnh `python main.py --test`, lấy trung bình thời gian thực thi giữa các cặp điểm ngẫu nhiên trên khuôn viên trường.
