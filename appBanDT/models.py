from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Bảng DanhMuc
class DanhMuc(models.Model):
    MaDanhMuc = models.AutoField(primary_key=True)
    TenDanhMuc = models.CharField(max_length=100, unique=True)  # VD: "Điện thoại", "Laptop"

    def __str__(self):
        return self.TenDanhMuc

# Bảng Thương Hiệu
class ThuongHieu(models.Model):
    MaThuongHieu = models.AutoField(primary_key=True)
    TenThuongHieu = models.CharField(max_length=100, unique=True)  # VD: "Apple", "Samsung"

    def __str__(self):
        return self.TenThuongHieu

# Bảng Dòng Sản Phẩm
class DongSanPham(models.Model):
    MaDongSanPham = models.AutoField(primary_key=True)
    TenDongSanPham = models.CharField(max_length=100)  # VD: "iPhone 11", "iPhone 12"
    ThuongHieu = models.ForeignKey(ThuongHieu, on_delete=models.CASCADE)  # Liên kết với thương hiệu
    DanhMuc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.DanhMuc is None:
            dien_thoai, created = DanhMuc.objects.get_or_create(TenDanhMuc="Điện thoại")
            self.DanhMuc = dien_thoai
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ThuongHieu.TenThuongHieu} - {self.TenDongSanPham}"

# Bảng Sản Phẩm
class SanPham(models.Model):
    MaSanPham = models.AutoField(primary_key=True)
    TenSanPham = models.CharField(max_length=100)
    MaDanhMuc = models.ForeignKey(DanhMuc, on_delete=models.CASCADE)  # Liên kết danh mục
    DongSanPham = models.ForeignKey(DongSanPham, on_delete=models.CASCADE)  # Liên kết dòng sản phẩm
    MoTa = models.TextField()
    SoLuongKho = models.IntegerField(default=0)
    TrangThai = models.CharField(max_length=20)

    def __str__(self):
        return self.TenSanPham
    
# Bảng Màu Sắc
class MauSac(models.Model):
    MaMauSac = models.AutoField(primary_key=True)
    TenMauSac = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.TenMauSac

# Bảng Dung Lượng
class DungLuong(models.Model):
    MaDungLuong = models.AutoField(primary_key=True)
    DungLuong = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.DungLuong

# Bảng Giá Theo Màu và Dung Lượng
class GiaSanPham(models.Model):
    MaGiaSanPham = models.AutoField(primary_key=True)
    MaSanPham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    MaMauSac = models.ForeignKey(MauSac, on_delete=models.CASCADE)
    MaDungLuong = models.ForeignKey(DungLuong, on_delete=models.CASCADE)
    GiaSanPham = models.FloatField()

    def __str__(self):
        return f"{self.MaSanPham.TenSanPham} - {self.MaMauSac.TenMauSac} - {self.MaDungLuong.DungLuong}: {self.GiaSanPham} VND"

# Bảng Hình Ảnh Sản Phẩm
class HinhAnhSanPham(models.Model):
    MaHinhAnh = models.AutoField(primary_key=True)
    MaSanPham = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    MaMauSac = models.ForeignKey(MauSac, on_delete=models.CASCADE)
    LinkAnhSanPham = models.ImageField(upload_to='', null=True, blank=True)  


    def __str__(self):
        return f"Hình ảnh của {self.MaSanPham.TenSanPham} - {self.MaMauSac.TenMauSac}"
    
class DatHang(models.Model):
    MaDatHang = models.AutoField(primary_key=True)
    TenKhachHang = models.CharField(max_length=100)
    SoDienThoai = models.CharField(max_length=15)
    LoiNhan = models.TextField(blank=True, null=True)
    TrangThai = models.CharField(max_length=50, default="Chờ liên hệ")
    NguoiLienHe = models.CharField(max_length=100, null=True, blank=True)
    # Thay vì ForeignKey tới GiaSanPham, ta lưu trực tiếp mã sản phẩm
    MaSP = models.CharField(max_length=50, null=True, blank=True)  

    def __str__(self):
        return f"ĐH {self.MaDatHang} - {self.TenKhachHang} | Mã SP: {self.MaSP}"
    
class AnhKhachHang(models.Model):
    MaAnhKhachHang = models.AutoField(primary_key=True)
    LinkAnhKhachHang = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return f"Ảnh khách hàng {self.MaAnhKhachHang}"
    

class ThongSoKyThuat(models.Model):
    MaThongSo = models.AutoField(primary_key=True)
    SanPham = models.OneToOneField(SanPham, on_delete=models.CASCADE)  # Liên kết với bảng sản phẩm
    ManHinh = models.CharField(max_length=100, blank=True, null=True)
    HeDieuHanh = models.CharField(max_length=50, blank=True, null=True)
    CPU = models.CharField(max_length=100, blank=True, null=True)
    RAM = models.CharField(max_length=50, blank=True, null=True)
    BoNhoTrong = models.CharField(max_length=50, blank=True, null=True)
    CameraTruoc = models.CharField(max_length=50, blank=True, null=True)
    CameraSau = models.CharField(max_length=100, blank=True, null=True)
    TheSIM = models.CharField(max_length=100, blank=True, null=True)
    DungLuongPin = models.CharField(max_length=100, blank=True, null=True)
    CongKetNoi = models.CharField(max_length=100, blank=True, null=True)
    TrongLuong = models.CharField(max_length=50, blank=True, null=True)
    ChongNuoc = models.CharField(max_length=50, blank=True, null=True)
    TinhNangDacBiet = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Thông số kỹ thuật của {self.SanPham.TenSanPham}"