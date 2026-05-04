# 🚀 MLOps Starter Kit: Quản lý Dự án ML với Git & DVC

Repository này là một bản demo hoàn chỉnh hướng dẫn cách xây dựng một dự án Machine Learning chuẩn mực, giải quyết bài toán đau đầu nhất của các team Data: **Làm sao để quản lý version cho những file Dữ liệu (Data) và Mô hình (Model) nặng hàng Gigabyte?**

Giải pháp: Sử dụng **Git** để quản lý Source Code và **DVC (Data Version Control)** để quản lý Data/Model.

## 📑 Mục lục

1. [Tại sao lại cần repo này?](#-tại-sao-lại-cần-repo-này "null")
    
2. [Cấu trúc Repository](#-cấu-trúc-repository "null")
    
3. [Cài đặt & Khởi chạy (Dành cho người mới)](#️-cài-đặt--khởi-chạy "null")
    
4. [📚 Hướng dẫn Thực hành: 5 Use Cases Cốt lõi](#-hướng-dẫn-thực-hành-5-use-cases-cốt-lõi "null")
    
    - [Use Case 1: Tách bạch Git và DVC](#use-case-1-tách-bạch-git-và-dvc-the-basics "null")
        
    - [Use Case 2: Cỗ máy thời gian cho Dữ liệu](#use-case-2-cỗ-máy-thời-gian-cho-dữ-liệu-data-versioning "null")
        
    - [Use Case 3: Tự động hóa Pipeline](#use-case-3-tự-động-hóa-pipeline-reproducible-pipeline "null")
        
    - [Use Case 4: Làm việc nhóm (Remote Storage)](#use-case-4-làm-việc-nhóm-remote-storage "null")
        
    - [Use Case 5: Theo dõi thử nghiệm (Experiment Tracking)](#use-case-5-theo-dõi-thử-nghiệm-experiment-tracking "null")
        
5. [Giải ngố các khái niệm (Dành cho người mới)](#-giải-ngố-các-khái-niệm "null")
    
6. [Tài liệu tham khảo](#-tài-liệu-tham-khảo "null")
    

## 🤔 Tại sao lại cần repo này?

Khi làm Machine Learning, chúng ta thường chia sẻ code qua GitHub/GitLab. Nhưng **Git không được thiết kế để lưu file lớn**. Nếu bạn cố push file CSV 5GB hay file Model `.bin` 500MB lên GitHub, repo sẽ bị chậm, phình to, hoặc bị GitHub chặn (limit 100MB/file).

_Cách cũ:_ Gửi code qua Git, gửi Data qua Google Drive/Zalo ❌ (Dễ nhầm lẫn version, khó tái lập lại kết quả). _Cách chuẩn:_ Code lưu ở Git, Data lưu qua DVC (giấu vào S3/Google Drive tự động) ✅.

## 📂 Cấu trúc Repository

Dự án được tổ chức theo chuẩn Clean Architecture cơ bản cho ML:

```
dvc-housing-demo/
├── .git/                   # Git quản lý code
├── .dvc/                   # DVC quản lý cache & cấu hình
├── data/
│   ├── raw/                # Dữ liệu gốc (Được DVC track)
│   └── processed/          # Dữ liệu sau tiền xử lý (Được DVC track)
├── models/                 # Model weights lưu tại đây (Được DVC track)
├── src/                    # Source code Python (Được Git track)
│   ├── data_prep.py        # Script clean data
│   ├── train.py            # Script train model
│   └── evaluate.py         # Script đánh giá
├── dvc.yaml                # File định nghĩa Pipeline các bước chạy
├── params.yaml             # File chứa Hyperparameters cho model
├── pyproject.toml          # File quản lý thư viện (dùng uv)
└── README.md
```

## 🛠️ Cài đặt & Khởi chạy

Để tự tay trải nghiệm repo này, bạn cần cài đặt `Python 3.8+` và `git` trên máy. Chúng tôi khuyến nghị sử dụng `uv` (một trình quản lý package cực nhanh) hoặc `pip` truyền thống.

**Bước 1: Clone repo về máy**

```
git clone <URL_CỦA_REPO_NÀY>
cd dvc-housing-demo
```

**Bước 2: Cài đặt môi trường** _(Sử dụng môi trường ảo venv cơ bản)_

```
python3 -m venv .venv
source .venv/bin/activate  # Trên Windows dùng: .venv\Scripts\activate
pip install dvc pandas scikit-learn catboost pyyaml
```

**Bước 3: Tải dữ liệu về (Mô phỏng DVC Pull)** _(Nếu chủ repo đã cấu hình remote storage, bạn chỉ cần gõ lệnh này để lấy toàn bộ data/model về)_

```
dvc pull
```

## 📚 Hướng dẫn Thực hành: 5 Use Cases Cốt lõi

Sau khi đã setup xong môi trường, hãy tuần tự thực hiện các bước dưới đây để hiểu sức mạnh của hệ thống này.

### Use Case 1: Tách bạch Git và DVC (The Basics)

_Làm thế nào để DVC track một file CSV nặng mà không làm nặng Git?_

1. Giả sử bạn có file `data/raw/dataset.csv`. Chạy lệnh sau để báo DVC quản lý nó:
    
    ```
    dvc add data/raw/dataset.csv
    ```
    
2. Bạn sẽ thấy DVC sinh ra một file nhỏ xíu tên là `dataset.csv.dvc`. Mở nó ra xem, bạn sẽ thấy nó chỉ chứa 1 đoạn mã Hash MD5.
    
3. Bây giờ, hãy nói với Git rằng: _"Hãy theo dõi cái file `.dvc` nhỏ xíu này, còn file CSV to đùng kia để DVC lo"_:
    
    ```
    git add data/raw/dataset.csv.dvc data/raw/.gitignore
    git commit -m "track data using DVC"
    ```
    

### Use Case 2: Cỗ máy thời gian cho Dữ liệu (Data Versioning)

_Data Engineer lỡ tay làm hỏng dữ liệu. Làm sao để quay lại bản ngày hôm qua?_

1. Cố tình làm hỏng file data bằng cách thêm 1 dòng dữ liệu rác:
    
    ```
    echo "9999999,2024,10,999999999" >> data/raw/dataset.csv
    dvc add data/raw/dataset.csv
    git add data/raw/dataset.csv.dvc
    git commit -m "update data with outlier"
    ```
    
2. Ôi không, data hỏng rồi! Để quay lại bản commit trước đó, thực hiện 2 lệnh:
    
    ```
    git checkout HEAD~1  # Quay Git về commit cũ
    dvc checkout         # Bảo DVC: "Hãy khôi phục file CSV vật lý cho khớp với Git"
    ```
    
3. Mở file `dataset.csv` lên, dòng dữ liệu rác đã biến mất!
    

### Use Case 3: Tự động hóa Pipeline (Reproducible Pipeline)

_Mỗi lần đổi tham số, tôi không biết phải chạy file Python nào trước, file nào sau._

1. Mở file `dvc.yaml`. Đây là bản đồ (Pipeline) định nghĩa thứ tự chạy: `prepare` -> `train` -> `evaluate`.
    
2. Mở file `params.yaml`, sửa thử `learning_rate` từ `0.05` thành `0.1`.
    
3. Chạy lệnh ma thuật:
    
    ```
    dvc repro
    ```
    

> **💡 Điều gì vừa xảy ra?** DVC cực kỳ thông minh. Nó nhận thấy dữ liệu gốc không đổi, nên nó **BỎ QUA** bước `data_prep.py` (bước có thể tốn hàng giờ), và chỉ chạy lại bước `train.py` và `evaluate.py`.

### Use Case 4: Làm việc nhóm (Remote Storage)

_Làm sao để đẩy file CSV 5GB này cho đồng nghiệp mà không xài USB?_

1. Tạo một thư mục tạm trên máy tính để giả làm máy chủ Cloud (AWS S3 / Google Drive):
    
    ```
    mkdir -p /tmp/dvc-remote-storage
    dvc remote add -d myremote /tmp/dvc-remote-storage
    ```
    
2. Đẩy Dữ liệu vật lý lên "Cloud":
    
    ```
    dvc push
    ```
    
3. Đồng nghiệp của bạn sau khi `git clone` repo này về, họ chỉ cần gõ `dvc pull`, toàn bộ data và model sẽ tự động tải về đúng vị trí.
    

### Use Case 5: Theo dõi thử nghiệm (Experiment Tracking)

_Làm sao để so sánh kết quả khi tôi thay đổi tham số liên tục?_

1. Chạy 2 thử nghiệm với độ sâu cây (depth) khác nhau:
    
    ```
    dvc exp run -S train.depth=4
    dvc exp run -S train.depth=8
    ```
    
2. Xem bảng so sánh kết quả trực tiếp trên Terminal:
    
    ```
    dvc exp show
    ```
    

## 🧠 Giải ngố các khái niệm

Nếu bạn là người mới, dưới đây là giải thích các thuật ngữ được dùng trong repo này:

- **Reproducibility (Tính tái lập):** Khả năng mà một người khác tải code của bạn về, chạy lệnh, và ra được kết quả/model y hệt 100% như bạn đã làm. Điều kiện tiên quyết để AI được đưa lên Production.
    
- **Metadata (File `.dvc`):** Là "dữ liệu mô tả dữ liệu". Thay vì lưu cái ảnh 5MB, DVC lưu một file text ghi là "Cái ảnh này nặng 5MB, ID của nó là XYZ". Git sẽ đọc file text này.
    
- **DVC Cache:** Khi bạn gõ `dvc add`, file gốc của bạn thực ra bị DVC lén giấu vào thư mục ẩn `.dvc/cache`. File bạn đang thấy trên màn hình thực chất chỉ là một "Hard link" (đường dẫn ảo) trỏ tới cache đó.
    
- **DAG (Directed Acyclic Graph):** Đồ thị có hướng không tuần hoàn. Trong `dvc.yaml`, DVC dùng DAG để hiểu rằng: Bước Train phụ thuộc vào Data Prep, do đó bắt buộc phải có Data Prep thì mới được chạy Train.
    
- **Hyperparameters (Siêu tham số):** Các thông số cấu hình model (ví dụ: learning rate, số vòng lặp) được lưu trong `params.yaml`. Việc tách chúng ra file YAML giúp ta quản lý và tinh chỉnh dễ dàng mà không cần lục tìm trong code Python.
    

## 📚 Tài liệu tham khảo

Để đào sâu hơn, bạn nên đọc các tài liệu chính thức cực kỳ chất lượng sau:

1. [**Get Started với DVC**](https://dvc.org/doc/start "null")**:** Hướng dẫn chính thức, cực kỳ dễ hiểu bằng tiếng Anh.
    
2. [**DVC Pipeline (dvc.yaml)**](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files "null")**:** Cách viết file pipeline chi tiết.
    
3. [**Data Versioning Explained**](https://dvc.org/doc/use-cases/versioning-data-and-models "null")**:** Giải thích chuyên sâu về cơ chế hash MD5 của DVC.
    
4. [**CatBoost Documentation**](https://catboost.ai/en/docs/ "null")**:** Thư viện Machine Learning (Gradient Boosting) được sử dụng để demo trong repo này.
    
5. [**Git Checkout & Lịch sử**](https://git-scm.com/docs/git-checkout "null")**:** Nắm vững Git là điều kiện bắt buộc trước khi học DVC.