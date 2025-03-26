from django.contrib import messages
from django.contrib import admin
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.urls import path, reverse
from django.utils.html import format_html  
from .models import (
    AnhKhachHang, DanhMuc, ThongSoKyThuat, ThuongHieu, DongSanPham,
    SanPham, MauSac, DungLuong, GiaSanPham,
    HinhAnhSanPham, DatHang
)

#giao diện cho ảnh khách hàng
class AnhKhachHangAdmin(admin.ModelAdmin):
    list_display = ('MaAnhKhachHang', 'xemanh')
    readonly_fields = ('preview_image',)  # Hiển thị ảnh trong trang chi tiết

    def xemanh(self, obj):
        if obj.LinkAnhKhachHang:
            return format_html('<img src="{}" width="80" height="80"/>', obj.LinkAnhKhachHang.url)
        return "Chưa có ảnh"

    xemanh.short_description = "Hình ảnh"

    def preview_image(self, obj):
        if obj.LinkAnhKhachHang:
            return format_html('<img id="preview-img" src="{}" width="200" height="200"/>', obj.LinkAnhKhachHang.url)
        return format_html('<img id="preview-img" src="" width="200" height="200" style="display:none"/>')

    preview_image.short_description = "Xem trước ảnh"

    class Media:
        js = ('assets/js/admin.js',)  # Gọi file JavaScript tùy chỉnh
admin.site.register(AnhKhachHang, AnhKhachHangAdmin)

class TrangThaiFilter(admin.SimpleListFilter):
    title = 'Trạng thái'  # Tiêu đề bộ lọc
    parameter_name = 'trang_thai'

    def lookups(self, request, model_admin):
        return [
            ('cho_lien_he', 'Chờ liên hệ'),
            ('da_lien_he', 'Đã liên hệ'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'cho_lien_he':
            return queryset.filter(TrangThai='Chờ liên hệ')
        if self.value() == 'da_lien_he':
            return queryset.filter(TrangThai='Đã liên hệ')

# Giao diện Admin cho DatHang
class DatHangAdmin(admin.ModelAdmin):
    list_display = ('MaDatHang', 'TenKhachHang', 'SoDienThoai', 'TrangThai', 'MaSP', 'NguoiLienHe', 'danh_dau_da_lien_he')
    list_filter = ('TrangThai',)
    readonly_fields = ('TrangThai', 'get_sanpham', 'get_gia', 'get_mausac', 'get_dungluong', 'get_hinhanh')

    def get_readonly_fields(self, request, obj=None):
        """ Khi vào chi tiết đơn hàng thì trạng thái có thể chỉnh sửa """
        if obj:  # Nếu đang sửa một đơn hàng
            return ('MaDatHang', 'TenKhachHang', 'SoDienThoai', 'MaSP', 'get_sanpham', 'get_gia', 'get_mausac', 'get_dungluong', 'get_hinhanh')  # Giữ các field này readonly
        return self.readonly_fields

    def get_sanpham(self, obj):
        try:
            sanpham = SanPham.objects.get(MaSanPham=obj.MaSP)
            return sanpham.TenSanPham
        except SanPham.DoesNotExist:
            return "Không tìm thấy"
    get_sanpham.short_description = "Sản phẩm"

    # Hiển thị Giá
    def get_gia(self, obj):
        try:
            gia_sp = GiaSanPham.objects.get(MaSanPham=obj.MaSP)
            return f"{gia_sp.GiaSanPham:,.0f} VND"
        except GiaSanPham.DoesNotExist:
            return "Không có giá"
    get_gia.short_description = "Giá"

    # Hiển thị Màu sắc
    def get_mausac(self, obj):
        try:
            gia_sp = GiaSanPham.objects.get(MaSanPham=obj.MaSP)
            return gia_sp.MaMauSac.TenMauSac
        except GiaSanPham.DoesNotExist:
            return "Không có màu"
    get_mausac.short_description = "Màu sắc"

    # Hiển thị Dung lượng
    def get_dungluong(self, obj):
        try:
            gia_sp = GiaSanPham.objects.get(MaSanPham=obj.MaSP)
            return gia_sp.MaDungLuong.DungLuong
        except GiaSanPham.DoesNotExist:
            return "Không có dung lượng"
    get_dungluong.short_description = "Dung lượng"

    # Hiển thị hình ảnh sản phẩm
    def get_hinhanh(self, obj):
        try:
            hinhanh = HinhAnhSanPham.objects.filter(MaSanPham=obj.MaSP).first()
            if hinhanh and hinhanh.LinkAnhSanPham:
                return format_html('<img src="{}" width="80px" height="80px" />', hinhanh.LinkAnhSanPham.url)
            return "Không có ảnh"
        except HinhAnhSanPham.DoesNotExist:
            return "Không có ảnh"
    get_hinhanh.short_description = "Hình ảnh"

    # Hàm xử lý khi ấn vào nút "Đã liên hệ"
    def danh_dau_da_lien_he(self, obj):
        if obj.TrangThai != "Đã liên hệ":
            return format_html('<a class="button" href="{}">Đã liên hệ</a>', f"mark-contacted/{obj.pk}")
        return "✅ Đã liên hệ"
    
    danh_dau_da_lien_he.short_description = "Hành động"
    danh_dau_da_lien_he.allow_tags = True

    # Thêm URL tùy chỉnh để cập nhật trạng thái
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('mark-contacted/<int:order_id>/', self.mark_contacted, name="mark-contacted"),
        ]
        return custom_urls + urls

    # Hàm xử lý cập nhật trạng thái đơn hàng
    def mark_contacted(self, request, order_id):
        order = DatHang.objects.get(pk=order_id)
        if order.TrangThai != "Đã liên hệ":
           order.TrangThai = "Đã liên hệ"
           order.NguoiLienHe = request.user.username  # Lưu tài khoản admin đã nhấn nút
           order.save()
           self.message_user(
            request, 
            f"✅ Đơn hàng {order.MaDatHang} đã được đánh dấu là 'Đã liên hệ' bởi {request.user.username}.", 
            level=messages.SUCCESS
        )
        return redirect(request.META.get('HTTP_REFERER', 'admin:appBanDT_dathang_changelist'))

admin.site.register(DatHang, DatHangAdmin)

class GiaSanPhamInline(admin.TabularInline):
    model = GiaSanPham

    def get_extra(self, request, obj=None, **kwargs):
        """Nếu sản phẩm đã có giá thì không hiển thị dòng trống"""
        return 0 if obj and GiaSanPham.objects.filter(MaSanPham=obj).exists() else 1


class HinhAnhSanPhamInline(admin.TabularInline):
    model = HinhAnhSanPham
    readonly_fields = ('preview_image',)
    def xem_anh(self, obj):
        if obj.LinkAnhSanPham:
            return format_html('<img src="{}" width="80" height="80"/>', obj.LinkAnhSanPham.url)
        return "Chưa có ảnh"

    xem_anh.short_description = "Hình ảnh"

    def preview_image(self, obj):
        if obj.LinkAnhSanPham:
            return format_html('<img id="preview-img" src="{}" width="200" height="200"/>', obj.LinkAnhSanPham.url)
        return format_html('<img id="preview-img" src="" width="200" height="200" style="display:none"/>')

    preview_image.short_description = "Xem trước ảnh"

    class Media:
        js = ('assets/js/admin.js',)

    def get_extra(self, request, obj=None, **kwargs):
        """Nếu sản phẩm đã có hình ảnh thì không hiển thị dòng trống"""
        return 0 if obj and HinhAnhSanPham.objects.filter(MaSanPham=obj).exists() else 1
#giao diện sản phẩm

class ThongSoKyThuatInline(admin.StackedInline):  
    model = ThongSoKyThuat  
    extra = 1  # Hiển thị một form trống nếu sản phẩm chưa có thông số

class SanPhamAdmin(admin.ModelAdmin):
    list_display = ('MaSanPham', 'TenSanPham', 'MaDanhMuc', 'SoLuongKho', 'TrangThai', 'toggle_trang_thai', 'suasp')
    list_filter = ('TrangThai',)
    search_fields = ('TenSanPham',)
    inlines = [GiaSanPhamInline, HinhAnhSanPhamInline, ThongSoKyThuatInline]


    def toggle_trang_thai(self, obj):
        """Hiển thị nút Ngưng bán hoặc Bán lại dựa trên trạng thái"""
        if obj.TrangThai == "Đang bán":
            return format_html('<a class="button" style="color:red;" href="ban-lai-ngung-ban/{}/">Ngưng bán</a>', obj.MaSanPham)
        else:
            return format_html('<a class="button" style="color:black;" href="ban-lai-ngung-ban/{}/">Bán lại</a>', obj.MaSanPham)

    toggle_trang_thai.short_description = "Hành động"
    
    def suasp(self, obj):
        """Hiển thị nút sửa"""
        edit_url = reverse('admin:appBanDT_sanpham_change', args=[obj.MaSanPham])
        return format_html('<a class="button" style="color:blue;" href="{}">Sửa</a>', edit_url)

    suasp.short_description = "Chỉnh sửa"

    def get_urls(self):
        """Tạo URL tùy chỉnh để cập nhật trạng thái"""
        urls = super().get_urls()
        custom_urls = [
            path('ban-lai-ngung-ban/<int:product_id>/', self.ban_lai_ngung_ban, name="ban-lai-ngung-ban"),
        ]
        return custom_urls + urls

    def ban_lai_ngung_ban(self, request, product_id):
        """Hàm xử lý khi nhấn nút Ngưng bán hoặc Bán lại"""
        product = SanPham.objects.get(pk=product_id)
        if product.TrangThai == "Đang bán":
            product.TrangThai = "Ngưng bán"
            messages.success(request, f"❌ Sản phẩm {product.TenSanPham} đã ngưng bán.")
        else:
            product.TrangThai = "Đang bán"
            messages.success(request, f"✅ Sản phẩm {product.TenSanPham} đã được bán lại.")
        product.save()
        return redirect(request.META.get('HTTP_REFERER', 'admin:appBanDT_sanpham_changelist'))
    

admin.site.register(SanPham, SanPhamAdmin)



#giao diện ảnh sản phẩm
class HinhAnhSanPhamAdmin(admin.ModelAdmin):
    list_display = ('MaHinhAnh', 'MaSanPham', 'xem_anh')
    readonly_fields = ('preview_image',)  # Xem trước ảnh trong trang chi tiết

    def xem_anh(self, obj):
        if obj.LinkAnhSanPham:
            return format_html('<img src="{}" width="80" height="80"/>', obj.LinkAnhSanPham.url)
        return "Chưa có ảnh"

    xem_anh.short_description = "Hình ảnh"

    def preview_image(self, obj):
        if obj.LinkAnhSanPham:
            return format_html('<img id="preview-img" src="{}" width="200" height="200"/>', obj.LinkAnhSanPham.url)
        return format_html('<img id="preview-img" src="" width="200" height="200" style="display:none"/>')

    preview_image.short_description = "Xem trước ảnh"

    class Media:
        js = ('assets/js/admin.js',)  # Nếu cần JavaScript tùy chỉnh

# Đăng ký HinhAnhSanPham với Admin
admin.site.register(HinhAnhSanPham, HinhAnhSanPhamAdmin)
# Đăng ký các model vào trang admin
admin.site.register(DanhMuc)

admin.site.register(ThuongHieu)

admin.site.register(DongSanPham)


admin.site.register(MauSac)
admin.site.register(DungLuong)
admin.site.register(GiaSanPham)
admin.site.register(ThongSoKyThuat)




#rảnh viết thêm chức năng thêm sửa xóa, nhanh lắm
# hiển thị hình ảnh
# phần quyền 