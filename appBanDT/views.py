import os
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
import re

from BanDienThoai import settings
from .models import AnhKhachHang, DanhMuc, DatHang, DungLuong, GiaSanPham, HinhAnhSanPham, MauSac, SanPham, DongSanPham, ThongSoKyThuat  

def extract_number(name):
    """Hàm trích xuất số từ tên dòng sản phẩm, nếu không có số thì đặt giá trị lớn"""
    match = re.search(r'\d+', name)  # Tìm số trong tên
    return int(match.group()) if match else float('inf')  # Nếu không có số, đặt giá trị lớn

def trangchu(request):
    sanphams = SanPham.objects.filter(TrangThai="Đang bán").order_by('-MaSanPham') 
    dongsanphams = DongSanPham.objects.all()
    danhmucs = DanhMuc.objects.all()  
    anhkhachhang = AnhKhachHang.objects.all()

    # Sắp xếp danh sách dòng sản phẩm theo số trong tên
    dongsanphams_sorted = sorted(dongsanphams, key=lambda d: extract_number(d.TenDongSanPham))

    return render(request, 'app/trangchu.html', {
        'sanphams': sanphams,
        'dongsanphams': dongsanphams_sorted,
        'danhmucs': danhmucs,  
        'anhkhachhang': anhkhachhang,
    })

def sanpham(request, masp=None):
    sanpham = None
    sanpham_lienquan = []
    dongsanphams = DongSanPham.objects.all()
    sanphams = SanPham.objects.filter(TrangThai="Đang bán").order_by('-MaSanPham')
    anhkhachhang = AnhKhachHang.objects.all()

    dungluong = {}
    mausac_gia_anh = {}

    # Lấy dung lượng và màu sắc từ URL
    dungluong_id = request.GET.get("dungluong")
    mausac_id = request.GET.get("mausac")
    thongso_kythuat = None

    if masp:
        sanpham = get_object_or_404(SanPham, MaSanPham=masp)
        sanpham_lienquan = SanPham.objects.filter(DongSanPham=sanpham.DongSanPham).exclude(MaSanPham=sanpham.MaSanPham)[:3]
        thongso_kythuat = ThongSoKyThuat.objects.filter(SanPham=sanpham).first()

        # Kiểm tra danh mục của sản phẩm
        is_phukien = sanpham.DongSanPham.DanhMuc.TenDanhMuc == "Phụ kiện"

        

        # Chỉ lấy danh sách dung lượng nếu sản phẩm không phải là "Phụ kiện"
        if not is_phukien:
            gia_cung_dongsanpham = GiaSanPham.objects.filter(MaSanPham__DongSanPham=sanpham.DongSanPham)
            for gia in gia_cung_dongsanpham:
                dungluong_key = gia.MaDungLuong.DungLuong
                if dungluong_key not in dungluong:
                    dungluong[dungluong_key] = gia

        # Lọc sản phẩm theo cả dung lượng và màu sắc
        sanpham_duoc_chon = None
        if dungluong_id and mausac_id:
            sanpham_duoc_chon = GiaSanPham.objects.filter(
                MaSanPham__DongSanPham=sanpham.DongSanPham,
                MaDungLuong=dungluong_id,
                MaMauSac__TenMauSac=mausac_id
            ).first()
        elif dungluong_id:
            sanpham_duoc_chon = GiaSanPham.objects.filter(
                MaSanPham__DongSanPham=sanpham.DongSanPham,
                MaDungLuong=dungluong_id
            ).first()
        elif mausac_id:
            sanpham_duoc_chon = GiaSanPham.objects.filter(
                MaSanPham__DongSanPham=sanpham.DongSanPham,
                MaMauSac__TenMauSac=mausac_id
            ).first()

        # Nếu tìm thấy sản phẩm phù hợp thì cập nhật sanpham
        if sanpham_duoc_chon:
            sanpham = sanpham_duoc_chon.MaSanPham

        # Lấy danh sách màu sắc của sản phẩm
        gia_cung_dungluong = gia_cung_dongsanpham.filter(MaDungLuong=dungluong_id) if dungluong_id else sanpham.giasanpham_set.all()
        for gia in gia_cung_dungluong:
            hinh_anh = HinhAnhSanPham.objects.filter(MaSanPham=gia.MaSanPham, MaMauSac=gia.MaMauSac).first()
            mausac_gia_anh[gia.MaMauSac.TenMauSac] = {
                "gia": gia.GiaSanPham,
                "hinh_anh": hinh_anh.LinkAnhSanPham.url if hinh_anh else None
            }

    return render(request, 'app/sanpham.html', {
        'sanpham': sanpham,
        'sanpham_lienquan': sanpham_lienquan,
        'dongsanphams': dongsanphams,
        'sanphams': sanphams,
        'anhkhachhang': anhkhachhang,
        'dungluong': dungluong.values() if not is_phukien else [],
        'mausac_gia_anh': mausac_gia_anh,
        'thongso_kythuat': thongso_kythuat,
        'is_phukien': is_phukien,  # Thêm biến này để kiểm tra trong template
    })

def dat_hang(request):
    if request.method == "POST":
        ten_khach_hang = request.POST.get("customer_name")
        so_dien_thoai = request.POST.get("customer_phone")
        loi_nhan = request.POST.get("customer_note", "")
        ma_sp = request.POST.get("MaSP")

        # Lưu vào CSDL với trạng thái mặc định là "Chờ liên hệ"
        dat_hang = DatHang.objects.create(
            TenKhachHang=ten_khach_hang,
            SoDienThoai=so_dien_thoai,
            LoiNhan=loi_nhan,
            MaSP=ma_sp,
            TrangThai="Chờ liên hệ"
        )

        return JsonResponse({"success": True, "message": "Đặt hàng thành công!"})

    dsdonhang = DatHang.objects.all().order_by("MaDatHang")
    return render(request, "app/quanlydathang.html", {"dathangs": dsdonhang})
    
    


def quanlysp(request):
    if request.method == "POST":
        MaSanPham = request.POST.get("MaSanPham")  # Lấy ID nếu có
        TenSanPham = request.POST.get("TenSanPham")
        MaDanhMuc = request.POST.get("MaDanhMuc")
        MaDongSanPham = request.POST.get("MaDongSanPham")
        SoLuongKho = request.POST.get("SoLuongKho")
        Gia = request.POST.get("GiaSanPham")
        MaMauSac = request.POST.get("MaMauSac")
        MaDungLuong = request.POST.get("MaDungLuong")
        HinhAnh = request.FILES.get("HinhAnhSanPham")
        MoTa = request.POST.get("MoTa")

        danhmuc = DanhMuc.objects.get(MaDanhMuc=MaDanhMuc)
        dongsanpham = DongSanPham.objects.get(MaDongSanPham=MaDongSanPham)
        mausac = MauSac.objects.get(MaMauSac=MaMauSac)
        dungluong = DungLuong.objects.get(MaDungLuong=MaDungLuong)

        if MaSanPham:  # Nếu có ID, thực hiện cập nhật
            sanpham = SanPham.objects.get(MaSanPham=MaSanPham)
            sanpham.TenSanPham = TenSanPham
            sanpham.MaDanhMuc = danhmuc
            sanpham.DongSanPham = dongsanpham
            sanpham.SoLuongKho = SoLuongKho
            sanpham.TrangThai = "Đang bán"
            sanpham.MoTa = MoTa
            sanpham.save()

            # Cập nhật bảng Giá Sản Phẩm
            gia_sp, created = GiaSanPham.objects.get_or_create(MaSanPham=sanpham, MaMauSac=mausac, MaDungLuong=dungluong)
            gia_sp.GiaSanPham = Gia
            gia_sp.save()

        else:  # Nếu không có ID, thêm mới sản phẩm
            sanpham = SanPham.objects.create(
                TenSanPham=TenSanPham,
                MaDanhMuc=danhmuc,
                DongSanPham=dongsanpham,
                SoLuongKho=SoLuongKho,
                TrangThai="Đang bán",
                MoTa=MoTa
            )

            GiaSanPham.objects.create(
                MaSanPham=sanpham,
                MaMauSac=mausac,
                MaDungLuong=dungluong,
                GiaSanPham=Gia
            )

        # Xử lý ảnh
        if HinhAnh:
            upload_dir = os.path.join(settings.MEDIA_ROOT)
            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, HinhAnh.name)
            with open(file_path, "wb+") as destination:
                for chunk in HinhAnh.chunks():
                    destination.write(chunk)

            image_url = f"{HinhAnh.name}"

            HinhAnhSanPham.objects.update_or_create(
                MaSanPham=sanpham,
                MaMauSac=mausac,
                defaults={"LinkAnhSanPham": image_url}
            )

        return redirect("quanlysp")

    # Lấy danh sách hiển thị
    sanphams = SanPham.objects.all()
    danhmucs = DanhMuc.objects.all()
    dongsanphams = DongSanPham.objects.all()
    mausacs = MauSac.objects.all()
    dungluongs = DungLuong.objects.all()

    return render(request, "app/quanlysp.html", {
        "sanphams": sanphams,
        "danhmucs": danhmucs,
        "dongsanphams": dongsanphams,
        "mausacs": mausacs,
        "dungluongs": dungluongs
    })

def capnhattrangthai(request, masp):
    if request.method == "POST":
        sanpham = get_object_or_404(SanPham, MaSanPham=masp)
        # Đảo trạng thái giữa "Đang bán" và "Ngưng bán"
        sanpham.TrangThai = "Ngưng bán" if sanpham.TrangThai == "Đang bán" else "Đang bán"
        sanpham.save()
        return JsonResponse({"status": "success", "new_trangthai": sanpham.TrangThai})
    return JsonResponse({"status": "error"}, status=400)

def capnhattrangthaidonhang(request, madonhang):
    if request.method == "POST":
        don_hang = get_object_or_404(DatHang, MaDatHang=madonhang)
        don_hang.TrangThai = "Đã liên hệ" if don_hang.TrangThai == "Chờ liên hệ" else "Chờ liên hệ"
        don_hang.save()

        return JsonResponse({"status": "success", "new_trangthai": don_hang.TrangThai})
    
    return JsonResponse({"status": "error", "message": "Yêu cầu không hợp lệ!"}, status=400)

def quanlyanh(request):
    if request.method == "POST":
        if "anhkhachhang" in request.FILES:  # Xử lý upload ảnh
            HinhAnh = request.FILES["anhkhachhang"]

            # Tạo thư mục lưu ảnh nếu chưa có
            upload_dir = os.path.join(settings.MEDIA_ROOT, "khachhang")
            os.makedirs(upload_dir, exist_ok=True)

            # Đường dẫn lưu ảnh
            file_path = os.path.join(upload_dir, HinhAnh.name)
            with open(file_path, "wb+") as destination:
                for chunk in HinhAnh.chunks():
                    destination.write(chunk)

            # Lưu vào database
            AnhKhachHang.objects.create(LinkAnhKhachHang=f"khachhang/{HinhAnh.name}")

            return redirect("quanlyanh")

        elif "xoa_anh" in request.POST:  # Xử lý xóa ảnh
            ma_anh = request.POST.get("xoa_anh")
            anh = get_object_or_404(AnhKhachHang, MaAnhKhachHang=ma_anh)

            # Xóa file ảnh khỏi thư mục
            file_path = os.path.join(settings.MEDIA_ROOT, str(anh.LinkAnhKhachHang))
            if os.path.exists(file_path):
                os.remove(file_path)

            # Xóa khỏi database
            anh.delete()
            return redirect("quanlyanh")

    anhs = AnhKhachHang.objects.all()
    return render(request, "app/quanlyanh.html", {"anhs": anhs})

def timsanpham(request):
    keyword = request.GET.get('keyword', '').strip()
    if keyword:
        sanphams = SanPham.objects.filter(TenSanPham__icontains=keyword)[:10]  
        results = []
        for sp in sanphams:
            hinh_anh = HinhAnhSanPham.objects.filter(MaSanPham=sp).first()  
            results.append({
                "id": sp.MaSanPham,
                "ten": sp.TenSanPham,
                "hinh_anh": hinh_anh.LinkAnhSanPham.url if hinh_anh else "/static/default.jpg",  
            })
        return JsonResponse({"sanphams": results})
    return JsonResponse({"sanphams": []})

def lienhe(request):
    anhkhachhang = AnhKhachHang.objects.all()
    sanphams = SanPham.objects.filter(TrangThai="Đang bán").order_by('-MaSanPham') 
    dongsanphams = DongSanPham.objects.all()
    danhmucs = DanhMuc.objects.all()  
    return render(request, 'app/lienhe.html',{
        'sanphams': sanphams,
        'dongsanphams': dongsanphams,
        'danhmucs': danhmucs,
        'anhkhachhang': anhkhachhang,
    })