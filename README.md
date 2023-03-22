# AMP Tool
**1. Tiện ích:**

- AMP Tool sẽ có chức năng chính là lọc toàn bộ thông tin cần thiết để việc recon với anh em pentest trở nên dễ dàng hơn bao giờ hết
- Ngoài ra tool vẫn đang được phát triển thêm các tính năng về Scan Vuln tự động với đầu ra được lấy từ quá trình Recon tự động

**2. Giao diện:**

- Giao diện thân thiện, chạy trong terminal với kernel là Linux

- Dưới đây là hình ảnh demo của tool

![image](https://user-images.githubusercontent.com/61643034/220074840-4e54c363-7040-443b-b240-e47b2b0dcc6a.png)

**3. Hướng dẫn sử dụng**

- Đầu tiên, bạn cần sử dụng lệnh
  ```bash
  git clone https://github.com/w4rf0t/AMP-Tools.git ; cd AMP-Tools ; chmod +x AutoRecon/install.sh; ./AutoRecon/install.sh
  ```
để cài các requirements cần thiết cho chương trình

- Sau đấy ```censys config``` rồi nhập thông tin vào. Thông tin config bao gồm ```API Key``` và ```Secret Key``` như hình dưới. [**Lấy ở đây**](https://search.censys.io/account/api)
 
![image](https://user-images.githubusercontent.com/61643034/226777100-bcb50737-d0b3-44d2-a155-63f55f5d86ca.png)


- Cuối cùng chỉ cần ``python3 main.py`` và enjoy cái moment này :>
