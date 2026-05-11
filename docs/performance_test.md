# Báo cáo Kiểm thử Hiệu năng (Performance Test Report)

## Mục tiêu của Benchmark
Quá trình benchmark đánh giá khả năng mở rộng và hiệu quả của thuật toán Dijkstra khi xử lý các đồ thị lớn được sinh ngẫu nhiên.

## Giải thích về Đồ thị Benchmark
Benchmark không sử dụng bản đồ HUST thực tế mà sử dụng các đồ thị liên thông được sinh ngẫu nhiên:
1. **Tính liên thông**: Đầu tiên thêm $n-1$ cạnh cơ sở (base edges) để tạo thành chuỗi nối tiếp từ node 0 đến $n-1$, đảm bảo đồ thị luôn liên thông.
2. **Cạnh phụ**: Sau đó thêm các cạnh phụ ngẫu nhiên (extra edges) dựa trên yêu cầu từ tham số `--edges`.
3. **Tổng số cạnh**: Bằng số cạnh cơ sở cộng với số cạnh phụ thực tế thêm được.
4. **Tính ổn định**: Sử dụng `seed` để kết quả sinh đồ thị có thể tái lập và `runs` để thực hiện thuật toán nhiều lần nhằm lấy số liệu thống kê trung bình.

## Các thông số đo lường
- **Seed**: Hạt giống ngẫu nhiên.
- **Runs**: Số lần chạy thuật toán trên cùng một đồ thị.
- **Avg/Median/Min/Max runtime**: Các số liệu thống kê về thời gian thực thi (ms).

## Kết quả Benchmark Chi tiết

| Số node | Cạnh phụ yêu cầu | Cạnh phụ thêm được | Tổng số cạnh | Seed | Số lần chạy | Avg runtime (ms) | Median runtime (ms) | Min-Max runtime (ms) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.000 | 4.000 | 4.000 | 4.999 | 42 | 5 | 2.5499 | 2.5199 | 2.4970 - 2.6903 |
| 5.000 | 20.000 | 20.000 | 24.999 | 42 | 5 | 16.4899 | 16.1804 | 14.9043 - 18.6098 |
| 10.000 | 40.000 | 40.000 | 49.999 | 42 | 5 | 37.5876 | 37.7514 | 34.7941 - 40.6592 |

## Đánh giá hiệu năng
Thời gian chạy tăng trưởng ổn định theo quy luật $O((V+E) \log V)$. Việc sử dụng giá trị trung vị (Median) giúp loại bỏ ảnh hưởng của các giá trị ngoại lai, cho thấy hiệu năng thực tế rất ổn định ngay cả với đồ thị có 10.000 đỉnh.
