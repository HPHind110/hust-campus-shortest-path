# BÁO CÁO KỸ THUẬT: TÌM ĐƯỜNG ĐI NGẮN NHẤT TRONG KHUÔN VIÊN BÁCH KHOA (HUST)

**Thành viên:** Lập trình viên 1 (Core Programmer)

## 1. Vai trò trong nhóm
Trong dự án này, tôi đảm nhận vai trò **Lập trình viên chính (Core Programmer 1)**, chịu trách nhiệm về phần nền tảng kỹ thuật và thuật toán cốt lõi của ứng dụng. Các đầu việc cụ thể bao gồm:
- Thiết kế và cài đặt cấu trúc dữ liệu đồ thị (Graph).
- Cài đặt thuật toán Dijkstra tìm đường đi ngắn nhất.
- Xây dựng cơ chế truy vết đường đi (Path reconstruction).
- Phát triển các hàm xử lý dữ liệu đầu vào/đầu ra (loadData, saveData).
- Viết các test case và thực hiện kiểm thử hiệu năng (Performance test).
- Viết tài liệu kỹ thuật, mã giả (pseudocode) và phân tích độ phức tạp thuật toán.

## 2. Phân tích Input/Output
Hệ thống xử lý hai loại dữ liệu chính:

### Input:
- **Dữ liệu Node (hust_nodes.csv):** Chứa thông tin về các địa điểm bao gồm ID, tên, loại địa điểm (tòa nhà, cổng, hồ...), tọa độ (x, y) và mô tả ngắn.
- **Dữ liệu Edge (hust_edges.csv):** Chứa thông tin về các đoạn đường nối giữa hai địa điểm, trọng số (khoảng cách tính bằng mét) và tính chất đường (một chiều hoặc hai chiều).

### Output:
- **Kết quả tìm đường:** Trả về tổng khoảng cách ngắn nhất, danh sách các địa điểm đi qua theo thứ tự, số lượng node đã duyệt và thời gian thực thi (ms).
- **Visualization:** Hình ảnh sơ đồ đồ thị với đường đi ngắn nhất được làm nổi bật (nếu người dùng yêu cầu).

## 3. Mô hình hóa bản đồ HUST thành đồ thị (Graph)
Bản đồ khuôn viên Bách Khoa được mô hình hóa dưới dạng **đồ thị có trọng số (Weighted Graph)**:
- **Node (Đỉnh):** Đại diện cho các thực thể vật lý như cổng trường (North Gate, West Gate...), các tòa nhà (C1, D3, B1...), các địa điểm tiện ích (Thư viện Tạ Quang Bửu, Hồ Tiền, Căng tin, Sân vận động).
- **Edge (Cạnh):** Đại diện cho các lối đi bộ, đường nội bộ giữa hai địa điểm.
- **Weight (Trọng số):** Đại diện cho khoảng cách xấp xỉ tính bằng mét giữa hai đỉnh.
- **Hướng:** Đa số các cạnh là hai chiều (bidirectional), phù hợp với việc đi bộ trong khuôn viên.

*Lưu ý: Dữ liệu bản đồ HUST hiện tại là dữ liệu mô phỏng dựa trên vị trí tương đối và bản đồ công khai, không phải là số liệu đo đạc thực tế chính xác tuyệt đối.*

## 4. Lựa chọn cấu trúc dữ liệu: Danh sách kề (Adjacency List)
Tôi lựa chọn **Danh sách kề** để lưu trữ đồ thị thay vì Ma trận kề vì:
- **Tiết kiệm bộ nhớ:** Bản đồ khuôn viên trường học là một đồ thị thưa (mỗi địa điểm chỉ kết nối với một vài địa điểm lân cận). Danh sách kề chỉ tiêu tốn không gian $O(V + E)$.
- **Hiệu suất duyệt:** Khi thực hiện Dijkstra, việc tìm các nút lân cận diễn ra rất nhanh chóng, giúp tối ưu thời gian thực thi.

## 5. Sử dụng Hàng đợi ưu tiên (Priority Queue/Min-Heap)
Trong thuật toán Dijkstra, việc tìm nút có khoảng cách nhỏ nhất trong mỗi bước là cực kỳ quan trọng.
- Tôi sử dụng module `heapq` (Min-Heap) của Python để cài đặt Priority Queue.
- **Lý do:** Việc lấy ra phần tử nhỏ nhất chỉ mất $O(\log V)$, thay vì $O(V)$ nếu dùng mảng thông thường. Điều này giúp thuật toán đạt hiệu năng tối ưu, đặc biệt là khi mở rộng quy mô dữ liệu.

## 6. Giải thích thuật toán Dijkstra
Thuật toán hoạt động dựa trên cơ chế **"Thư giãn cạnh" (Edge Relaxation)**:
1. Khởi tạo khoảng cách tới nút gốc là 0, các nút khác là vô cùng ($\infty$).
2. Đưa nút gốc vào hàng đợi ưu tiên.
3. Chừng nào hàng đợi chưa trống:
   - Lấy nút $u$ có khoảng cách nhỏ nhất hiện tại.
   - Nếu đã tới đích, dừng lại.
   - Với mỗi hàng xóm $v$ của $u$, tính toán khoảng cách mới: $dist(v) = dist(u) + weight(u, v)$.
   - Nếu khoảng cách mới này nhỏ hơn khoảng cách hiện tại đang lưu cho $v$, cập nhật lại và đưa $v$ vào hàng đợi.
4. Lưu lại nút cha của mỗi nút để truy vết đường đi sau khi kết thúc.

## 7. Mã giả (Pseudocode)
```text
FUNCTION Dijkstra(Graph, StartNode, EndNode):
    CREATE a Priority Queue (PQ)
    CREATE a Map 'Distances' with all nodes set to Infinity
    CREATE a Map 'Parents' to track the path
    
    SET Distances[StartNode] = 0
    PUSH (0, StartNode) into PQ
    
    WHILE PQ is not empty:
        POP (current_distance, current_node) with smallest distance
        
        IF current_node == EndNode:
            BREAK (Target reached)
            
        IF current_distance > Distances[current_node]:
            CONTINUE (Skip outdated path)
            
        FOR each neighbor of current_node:
            weight = edge weight between current_node and neighbor
            new_distance = current_distance + weight
            
            IF new_distance < Distances[neighbor]:
                Distances[neighbor] = new_distance
                Parents[neighbor] = current_node
                PUSH (new_distance, neighbor) into PQ
                
    RETURN Distances[EndNode] and RECONSTRUCT_PATH(Parents, EndNode)
```

## 8. Phân tích độ phức tạp Big-O
- **Độ phức tạp thời gian:** $O((V + E) \log V)$
    - Duyệt qua mỗi đỉnh tối đa 1 lần ($V$).
    - Duyệt qua mỗi cạnh tối đa 1 lần ($E$).
    - Mỗi thao tác trên Heap mất $\log V$.
- **Độ phức tạp không gian:** $O(V + E)$
    - Lưu trữ danh sách kề và các cấu trúc phụ trợ (Distances, Parents).

## 9. Test case nhỏ (HUST Data)
**Kịch bản:** Tìm đường từ Cổng Bắc (NORTH_GATE) đến Sân vận động (STADIUM).
- **Kết quả thực tế:**
    - Tổng khoảng cách: 790.0 mét.
    - Đường đi: Cổng Bắc $\rightarrow$ C1 $\rightarrow$ C3 $\rightarrow$ C6 $\rightarrow$ C7 $\rightarrow$ C8 $\rightarrow$ B8 Gate $\rightarrow$ B1 $\rightarrow$ Sân vận động.
    - Số đỉnh đã duyệt: 27.
    - Thời gian thực thi: ~0.05 ms.

## 10. Performance test với dữ liệu lớn
Tôi đã thực hiện benchmark trên các đồ thị ngẫu nhiên quy mô lớn để kiểm tra giới hạn của hệ thống:
| Số Node | Số Cạnh | Thời gian thực thi (ms) |
| :--- | :--- | :--- |
| 1,000 | ~4,000 | 3.71 ms |
| 5,000 | ~20,000 | 6.87 ms |
| 10,000 | ~40,000 | 15.20 ms (ước tính) |

**Nhận xét:** Ngay cả với 5,000 địa điểm, thời gian phản hồi vẫn dưới 10ms, chứng tỏ thuật toán cài đặt cực kỳ hiệu quả và có khả năng mở rộng tốt.

## 11. Tính năng Visualization
Mặc dù dự án tập trung vào thuật toán core, tôi đã tích hợp thêm module `matplotlib` để:
- Vẽ sơ đồ các địa điểm theo tọa độ (x, y).
- Kết nối các địa điểm bằng các đường thẳng (cạnh).
- Tô màu đỏ và đánh dấu mũi tên cho đường đi ngắn nhất tìm được.
- Điều này giúp người dùng dễ dàng hình dung lộ trình trong thực tế.

## 12. Hạn chế của dữ liệu mô phỏng
- **Độ chính xác:** Khoảng cách được tính toán dựa trên tọa độ pixel mô phỏng và ước lượng, không phản ánh chính xác từng mét trên thực tế.
- **Tính thời gian thực:** Chưa tính đến các yếu tố như đường đang thi công, các tòa nhà đang đóng cửa hoặc mật độ người đi bộ.
- **Địa hình:** Đồ thị hiện tại giả định mặt phẳng 2D, chưa xét đến yếu tố độ cao hoặc đi xuyên qua tầng của các tòa nhà.

## 13. Hướng mở rộng
Nếu có cơ hội phát triển tiếp, tôi đề xuất:
- **Tích hợp GPS/OSM:** Sử dụng dữ liệu thực từ OpenStreetMap để có tọa độ kinh độ/vĩ độ chính xác.
- **Real-time Traffic:** Cập nhật trọng số cạnh dựa trên mật độ giao thông hoặc sự kiện thực tế trong trường.
- **Đa phương tiện:** Hỗ trợ tìm đường cho cả người đi bộ, xe đạp và xe máy (với các quy định cấm đường khác nhau).
- **Web/Mobile UI:** Xây dựng giao diện người dùng thân thiện hơn thay vì dòng lệnh (CLI).
