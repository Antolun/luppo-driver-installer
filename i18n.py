"""
Internationalization (i18n) module for Graphics Driver Installer.
Supports English (default) and Turkish, automatically selected based on system locale.
"""

import os
import locale
from PyQt6.QtCore import QLocale

# Current active language code ("en" or "tr")
_ACTIVE_LANG = "en"


def detect_system_language() -> str:
    """
    Detect system language code. Returns 'tr' if Turkish locale is detected,
    otherwise defaults to 'en'.
    """
    # 1. Check environment variables
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        val = os.environ.get(var, "")
        if val:
            lang_code = val.split(".")[0].split("_")[0].lower()
            if lang_code == "tr":
                return "tr"
            elif lang_code:
                return "en"

    # 2. Check QLocale
    try:
        sys_loc = QLocale.system().name()
        if sys_loc.lower().startswith("tr"):
            return "tr"
    except Exception:
        pass

    # 3. Check Python default locale
    try:
        loc, _ = locale.getdefaultlocale()
        if loc and loc.lower().startswith("tr"):
            return "tr"
    except Exception:
        pass

    return "en"


def get_language() -> str:
    """Return currently active language code."""
    return _ACTIVE_LANG


def set_language(lang: str):
    """Set active language ('en' or 'tr')."""
    global _ACTIVE_LANG
    if lang in TRANSLATIONS:
        _ACTIVE_LANG = lang


# Auto-detect language on module load
_ACTIVE_LANG = detect_system_language()


TRANSLATIONS = {
    "en": {
        # App Info
        "app_name": "LupuS Graphics Driver Installer",
        "app_subtitle": "Install, Remove, and Manage GPU Drivers on Pisi Linux / LupuS",
        
        # Header Bar
        "header_demo_inactive": " Demo: Inactive",
        "header_demo_active": " Demo: Active",
        "header_refresh": " Refresh",

        # Sidebar Navigation
        "nav_gpus": "🖥️  Graphics Cards",
        "nav_diagnostics": "📊  System Diagnostics",
        "nav_settings": "⚙️  Settings / Hybrid",
        "nav_logs": "📜  Operation Log",

        # Driver Database (Config)
        "driver_nvidia_prop_name": "NVIDIA Proprietary Driver (Latest / Recommended)",
        "driver_nvidia_prop_desc": "Official closed-source driver and CUDA support for modern NVIDIA graphics cards (GeForce GTX 10xx, RTX 20xx/30xx/40xx).",
        "driver_nvidia_open_name": "NVIDIA Open Kernel Driver",
        "driver_nvidia_open_desc": "Driver package with open source kernel modules for NVIDIA Turing and newer (RTX 20xx+) architectures.",
        "driver_nvidia_390_name": "NVIDIA Legacy Driver (390.xx)",
        "driver_nvidia_390_desc": "Legacy driver package for older generation NVIDIA graphics cards (GeForce 400/500/600/700 series).",
        "driver_nouveau_name": "Nouveau Open-Source Driver",
        "driver_nouveau_desc": "Free and open-source Nouveau graphics card driver developed by the community.",
        "driver_all_nvidia": "All NVIDIA Cards",

        "driver_amd_mesa_name": "Mesa AMDGPU Open-Source Stack (Recommended)",
        "driver_amd_mesa_desc": "High-performance free driver for AMD Radeon HD 7000, RX 400/500, Vega, RX 5000/6000/7000 series.",
        "driver_amd_legacy_name": "Mesa ATI / Radeon Legacy Driver",
        "driver_amd_legacy_desc": "Open-source DDX driver for legacy generation AMD/ATI Radeon (R100 - R700) graphics cards.",
        "driver_amd_legacy_series": "Radeon HD 6000 and earlier",

        "driver_intel_mesa_name": "Intel Graphics Open-Source Stack (Recommended)",
        "driver_intel_mesa_desc": "Vulkan ANV & Mesa OpenGL driver support for Intel HD/UHD/Iris Graphics and Arc GPUs.",
        "driver_intel_media_name": "Intel VA-API Video Acceleration Driver",
        "driver_intel_media_desc": "Intel iHD VA-API hardware video encoding and decoding (H.264, HEVC, VP9, AV1) driver.",
        "driver_intel_broadwell_plus": "Intel Broadwell and newer",

        "driver_vbox_name": "VirtualBox Guest Additions Graphics Driver",
        "driver_vbox_desc": "VirtualBox virtual machine display driver and resolution integration.",
        "driver_vmware_name": "VMware SVGA II Driver",
        "driver_vmware_desc": "Graphics display driver for VMware and ESXi virtual machines.",

        # Categories
        "cat_proprietary": "Proprietary",
        "cat_open_source_kernel": "Open Source Kernel",
        "cat_legacy": "Legacy",
        "cat_open_source": "Open Source",
        "cat_legacy_open_source": "Legacy Open Source",
        "cat_hw_acceleration": "Hardware Acceleration",
        "cat_virtualization": "Virtualization",
        "cat_general": "General",

        # DriverRow & GPUCard
        "badge_recommended": "Recommended",
        "badge_hybrid": "Hybrid Graphics",
        "driver_row_package": "Package: <b style='color:#cbd5e1'>{pkg}</b>",
        "driver_row_installed_ver": " | Installed Version: <b style='color:#34d399'>{ver}</b>",
        "driver_row_repo_ver": " | Repository Version: <b style='color:#94a3b8'>{ver}</b>",
        "status_installed": "INSTALLED",
        "status_installing": "Installing...",
        "status_removing": "Removing...",
        "status_not_installed": "Not Installed",
        "btn_remove": "Remove",
        "btn_install": "Install",
        "gpu_active_driver": "Active Driver: <b style='color:#38bdf8'>{driver}</b>",
        "gpu_opengl": "OpenGL: <b style='color:#cbd5e1'>{renderer}</b>",
        "gpu_vulkan_supported": "Vulkan: <b style='color:#34d399'>Supported</b>",
        "gpu_vulkan_not_supported": "Vulkan: <b style='color:#64748b'>Not Supported</b>",
        "gpu_available_drivers": "Available Driver Packages",
        "spec_not_specified": "Not specified",
        "badge_nvidia": "NVIDIA",
        "badge_amd": "AMD Radeon",
        "badge_intel": "Intel Graphics",
        "badge_generic": "Generic Graphics",

        # DriversView
        "view_executing_operation": "Executing operation...",
        "reboot_warning": "A system reboot is recommended for driver changes to take effect.",
        "no_gpus_found": "No compatible graphics cards found on the system.",
        "progress_scanning_gpus": "Scanning graphics cards...",
        "progress_querying_pisi": "Querying PiSi package database...",

        # LogViewer
        "log_title": "LIVE OPERATION LOG (LOG CONSOLE)",
        "log_autoscroll": "Auto-scroll",
        "log_clear": " Clear",
        "log_save": " Save Log",
        "log_save_dialog_title": "Save Log File",
        "log_save_error": "[ERROR] Failed to save log file: {error}",

        # SettingsView
        "settings_title": "SETTINGS & HYBRID GRAPHICS MANAGEMENT",
        "hybrid_profile_title": "NVIDIA Optimus / PRIME Hybrid Graphics Profile",
        "hybrid_profile_desc": "Change the active GPU profile used on dual-GPU (Laptop Optimus / Dual GPU) systems.",
        "lbl_graphics_mode": "Graphics Mode:",
        "hybrid_opt_prime": "NVIDIA PRIME Offload (Dynamic / Recommended)",
        "hybrid_opt_nv": "NVIDIA High Performance (Discrete GPU Only)",
        "hybrid_opt_integrated": "Integrated Graphics (Power Saving / Intel-AMD Only)",
        "btn_apply_profile": "Apply Profile",
        "pisi_mgmt_title": "PiSi Repository and Cache Management",
        "pisi_mgmt_desc": "Refresh PiSi package manager database or clear download cache.",
        "btn_update_repo": " Update Repositories (pisi update-repo)",
        "btn_clean_cache": " Clear Cache (pisi delete-cache)",
        "msg_hybrid_title": "Hybrid Graphics Profile",
        "msg_hybrid_text": "Graphics mode set to '{mode}'.\nLog out and log back in for changes to take effect.",
        "msg_pisi_cache_title": "PiSi Cache",
        "msg_pisi_cache_text": "PiSi package cache was successfully cleared.",

        # SysInfoView
        "sysinfo_title": "SYSTEM & GRAPHICS HARDWARE DIAGNOSTICS",
        "sysinfo_env_title": "Display Server & Kernel Information",
        "sysinfo_desktop": "Desktop Environment:",
        "sysinfo_session": "Session Type (Display Server):",
        "sysinfo_kernel": "Kernel:",
        "sysinfo_gl_title": "OpenGL Hardware Acceleration Status (glxinfo)",
        "sysinfo_vk_title": "Vulkan Graphics API Status (vulkaninfo)",
        "sysinfo_pci_title": "PCI Graphics Devices (lspci -vnn)",
        "sysinfo_gl_failed": "Failed to get glxinfo output.",
        "sysinfo_vk_failed": "Vulkan info unavailable or Vulkan not supported.",
        "sysinfo_pci_failed": "Failed to get lspci output.",

        # MainWindow Logs & Confirmations
        "log_demo_enabled": "[SYSTEM] Demo mode activated.",
        "log_demo_disabled": "[SYSTEM] Demo mode deactivated.",
        "log_scan_start": "[SYSTEM] Starting new hardware scan...",
        "log_scan_done": "[SYSTEM] Hardware and package database scan completed.",
        "dialog_install_title": "Driver Installation Confirmation",
        "dialog_install_msg": "Do you confirm installing package <b>{driver_name}</b> ({package_name})?\n\nExtra Driver Packages: {extra}",
        "none_str": "None",
        "dialog_remove_title": "Driver Removal Confirmation",
        "dialog_remove_msg": "Do you confirm removing package <b>{driver_name}</b> ({package_name}) from the system?",
        "log_install_req": "[PISI] Install request received: {pkg}",
        "log_remove_req": "[PISI] Remove request received: {pkg}",
        "log_repo_req": "[PISI] Repository update request received.",
        "version_updated": "Latest",
        "log_success": "[SUCCESS] {msg}",
        "dialog_success_title": "Operation Completed",
        "log_error": "[ERROR] Operation failed: {msg}",
        "dialog_error_title": "Operation Failed",
        "dialog_repo_success_title": "Repositories Updated",
        "dialog_repo_error_title": "Update Failed",

        # Backend Workers / Detectors / Pisi
        "worker_scan_start": "[SYSTEM] Starting hardware scan (lspci & glxinfo)...",
        "worker_scan_count": "[SYSTEM] Detected a total of {count} graphics card(s).",
        "worker_scan_gpu_item": "[HARDWARE] {vendor}: {model} (Driver: {driver})",
        "worker_pisi_querying": "[PISI] Querying driver package statuses from PiSi database...",
        "worker_pisi_status": "[PISI] {pkg}: Status -> {status} (Version: {version})",
        "worker_install_success": "{pkg} driver installed successfully!",
        "worker_install_fail": "{pkg} installation failed.",
        "worker_remove_success": "{pkg} package removed!",
        "worker_remove_fail": "{pkg} removal failed.",
        "worker_repo_success": "Repository database updated successfully!",
        "worker_repo_fail": "Repository update failed.",
        "unknown_vendor": "Unknown Vendor",
        "unknown_str": "Unknown",
        "default_str": "Default",

        # Pisi Backend messages
        "pisi_install_start": "Starting installation of {pkg_name} package...",
        "pisi_cmd_install": "[PISI] Install command: pisi install {cmd}",
        "pisi_verifying_repos": "[PISI] Verifying repository indices...",
        "pisi_downloading": "[PISI] Downloading: {pkg} ({size})",
        "pisi_unpacking": "[PISI] Unpacking packages and checking dependencies...",
        "pisi_copying_files": "[PISI] Copying driver files and compiling modules...",
        "pisi_updating_xorg": "[PISI] Updating Xorg and DKMS configuration...",
        "pisi_install_done": "[PISI] {pkg} installed successfully!",
        "pisi_install_comp_msg": "Installation completed successfully!",
        "pisi_install_comp_log": "[PISI] Operation completed successfully.",
        "pisi_err_exit_code": "Error! Exit code: {code}",
        "pisi_err_install_fail": "[ERROR] pisi install failed ({code})",
        "pisi_exception": "[EXCEPTION] {msg}",
        "pisi_remove_start": "Removing {pkg} package...",
        "pisi_cmd_remove": "[PISI] Remove command: pisi remove {pkg}",
        "pisi_checking_deps": "[PISI] Checking package dependencies...",
        "pisi_deleting_files": "[PISI] Deleting driver files from system...",
        "pisi_refreshing_mods": "[PISI] Refreshing system module configuration...",
        "pisi_remove_done": "[PISI] {pkg} package(s) removed!",
        "pisi_remove_comp_msg": "Package removed!",
        "pisi_remove_comp_log": "[PISI] Package deleted successfully.",
        "pisi_err_remove_fail": "[ERROR] pisi remove failed ({code})",
        "pisi_update_repos_start": "Updating repository databases...",
        "pisi_cmd_update_repo": "[PISI] Running pisi update-repo",
        "pisi_downloading_repos": "Downloading repositories...",
        "pisi_updating_repos_log": "[PISI] Updating core, main, contrib repositories...",
        "pisi_repos_updated_msg": "Repositories updated!",
        "pisi_repos_updated_log": "[PISI] Repository update completed.",
    },
    "tr": {
        # App Info
        "app_name": "LupuS Grafik Sürücü Yöneticisi",
        "app_subtitle": "Pisi Linux / LupuS Üzerinde GPU Sürücülerini Kurun, Kaldırın ve Yönetin",

        # Header Bar
        "header_demo_inactive": " Demo: Pasif",
        "header_demo_active": " Demo: Aktif",
        "header_refresh": " Yenile",

        # Sidebar Navigation
        "nav_gpus": "🖥️  Ekran Kartları",
        "nav_diagnostics": "📊  Sistem Teşhisi",
        "nav_settings": "⚙️  Ayarlar / Hibrit",
        "nav_logs": "📜  İşlem Günlüğü",

        # Driver Database (Config)
        "driver_nvidia_prop_name": "NVIDIA Proprietary Driver (Güncel / Önerilen)",
        "driver_nvidia_prop_desc": "NVIDIA modern ekran kartları (GeForce GTX 10xx, RTX 20xx/30xx/40xx) için resmi kapalı kaynak sürücü ve CUDA desteği.",
        "driver_nvidia_open_name": "NVIDIA Open Kernel Driver",
        "driver_nvidia_open_desc": "NVIDIA Turing ve daha yeni (RTX 20xx+) mimariler için açık kaynak kernel modüllerine sahip sürücü paketi.",
        "driver_nvidia_390_name": "NVIDIA Legacy Driver (390.xx)",
        "driver_nvidia_390_desc": "Eski nesil NVIDIA ekran kartları (GeForce 400/500/600/700 serisi) için legacy sürücü paketi.",
        "driver_nouveau_name": "Nouveau Open-Source Driver",
        "driver_nouveau_desc": "Topluluk tarafından geliştirilen özgür ve açık kaynak Nouveau ekran kartı sürücüsü.",
        "driver_all_nvidia": "Tüm NVIDIA Kartlar",

        "driver_amd_mesa_name": "Mesa AMDGPU Open-Source Stack (Önerilen)",
        "driver_amd_mesa_desc": "AMD Radeon HD 7000, RX 400/500, Vega, RX 5000/6000/7000 serisi için yüksek performanslı özgür sürücü.",
        "driver_amd_legacy_name": "Mesa ATI / Radeon Legacy Driver",
        "driver_amd_legacy_desc": "Eski nesil AMD/ATI Radeon (R100 - R700) ekran kartları için açık kaynak DDX sürücüsü.",
        "driver_amd_legacy_series": "Radeon HD 6000 ve öncesi",

        "driver_intel_mesa_name": "Intel Graphics Open-Source Stack (Önerilen)",
        "driver_intel_mesa_desc": "Intel HD/UHD/Iris Graphics ve Arc GPU'ları için Vulkan ANV & Mesa OpenGL sürücü desteği.",
        "driver_intel_media_name": "Intel VA-API Video Acceleration Driver",
        "driver_intel_media_desc": "Intel iHD VA-API donanımsal video kodlama ve çözme (H.264, HEVC, VP9, AV1) sürücüsü.",
        "driver_intel_broadwell_plus": "Intel Broadwell ve üzeri",

        "driver_vbox_name": "VirtualBox Guest Additions Graphics Driver",
        "driver_vbox_desc": "VirtualBox sanal makine ekran sürücüsü ve çözünürlük entegrasyonu.",
        "driver_vmware_name": "VMware SVGA II Driver",
        "driver_vmware_desc": "VMware ve ESXi sanal makineleri için grafik görüntüleme sürücüsü.",

        # Categories
        "cat_proprietary": "Kapalı Kaynak",
        "cat_open_source_kernel": "Açık Kaynak Çekirdek",
        "cat_legacy": "Eski Nesil",
        "cat_open_source": "Açık Kaynak",
        "cat_legacy_open_source": "Eski Nesil Açık Kaynak",
        "cat_hw_acceleration": "Donanım Hızlandırma",
        "cat_virtualization": "Sanal Devre",
        "cat_general": "Genel",

        # DriverRow & GPUCard
        "badge_recommended": "Önerilen",
        "badge_hybrid": "Hibrit Grafik",
        "driver_row_package": "Paket: <b style='color:#cbd5e1'>{pkg}</b>",
        "driver_row_installed_ver": " | Kurulu Sürüm: <b style='color:#34d399'>{ver}</b>",
        "driver_row_repo_ver": " | Depo Sürümü: <b style='color:#94a3b8'>{ver}</b>",
        "status_installed": "KURULU",
        "status_installing": "Kuruluyor...",
        "status_removing": "Kaldırılıyor...",
        "status_not_installed": "Kurulu Değil",
        "btn_remove": "Kaldır",
        "btn_install": "Yükle",
        "gpu_active_driver": "Aktif Sürücü: <b style='color:#38bdf8'>{driver}</b>",
        "gpu_opengl": "OpenGL: <b style='color:#cbd5e1'>{renderer}</b>",
        "gpu_vulkan_supported": "Vulkan: <b style='color:#34d399'>Destekli</b>",
        "gpu_vulkan_not_supported": "Vulkan: <b style='color:#64748b'>Desteklenmiyor</b>",
        "gpu_available_drivers": "Mevcut Sürücü Paketleri",
        "spec_not_specified": "Belirtilmedi",
        "badge_nvidia": "NVIDIA",
        "badge_amd": "AMD Radeon",
        "badge_intel": "Intel Graphics",
        "badge_generic": "Genel Grafik",

        # DriversView
        "view_executing_operation": "İşlem yürütülüyor...",
        "reboot_warning": "Sürücü değişikliklerinin geçerli olması için bilgisayarınızı yeniden başlatmanız önerilir.",
        "no_gpus_found": "Sistemde uyumlu grafik kartı bulunamadı.",
        "progress_scanning_gpus": "Grafik kartları taranıyor...",
        "progress_querying_pisi": "PiSi paket veritabanı sorgulanıyor...",

        # LogViewer
        "log_title": "CANLI İŞLEM GÜNLÜĞÜ (LOG CONSOLE)",
        "log_autoscroll": "Otomatik Kaydır",
        "log_clear": " Temizle",
        "log_save": " Günlüğü Kaydet",
        "log_save_dialog_title": "Günlük Dosyasını Kaydet",
        "log_save_error": "[HATA] Günlük dosyası kaydedilemedi: {error}",

        # SettingsView
        "settings_title": "AYARLAR VE HİBRİT GRAFİK YÖNETİMİ",
        "hybrid_profile_title": "NVIDIA Optimus / PRIME Hibrit Grafik Profili",
        "hybrid_profile_desc": "Çift ekran kartlı (Laptop Optimus / Dual GPU) sistemlerde kullanılan aktif GPU profilini değiştirin.",
        "lbl_graphics_mode": "Grafik Modu:",
        "hybrid_opt_prime": "NVIDIA PRIME Offload (Dinamik / Önerilen)",
        "hybrid_opt_nv": "NVIDIA Yüksek Performans (Sadece Harici GPU)",
        "hybrid_opt_integrated": "Entegre Grafik (Tasarruf Modu / Sadece Intel-AMD)",
        "btn_apply_profile": "Profili Uygula",
        "pisi_mgmt_title": "PiSi Depo ve Önbellek Yönetimi",
        "pisi_mgmt_desc": "PiSi paket yöneticisi veritabanını yenileyin veya indirme önbelleğini temizleyin.",
        "btn_update_repo": " Depoları Güncelle (pisi update-repo)",
        "btn_clean_cache": " Önbelleği Temizle (pisi delete-cache)",
        "msg_hybrid_title": "Hibrit Grafik Profili",
        "msg_hybrid_text": "Grafik modu '{mode}' olarak ayarlandı.\nDeğişikliklerin etkili olması için oturumu kapatıp yeniden açın.",
        "msg_pisi_cache_title": "PiSi Önbelleği",
        "msg_pisi_cache_text": "PiSi paket önbelleği başarıyla temizlendi.",

        # SysInfoView
        "sysinfo_title": "SİSTEM VE GRAFİK DONANIM TEŞHİSİ",
        "sysinfo_env_title": "Görüntü Sunucusu ve Çekirdek (Kernel) Bilgisi",
        "sysinfo_desktop": "Masaüstü Ortamı:",
        "sysinfo_session": "Oturum Türü (Display Server):",
        "sysinfo_kernel": "Çekirdek (Kernel):",
        "sysinfo_gl_title": "OpenGL Donanım Hızlandırma Durumu (glxinfo)",
        "sysinfo_vk_title": "Vulkan Grafik API Durumu (vulkaninfo)",
        "sysinfo_pci_title": "PCI Grafik Aygıtları (lspci -vnn)",
        "sysinfo_gl_failed": "glxinfo çıktısı alınamadı.",
        "sysinfo_vk_failed": "Vulkan bilgisi alınamadı veya Vulkan desteklenmiyor.",
        "sysinfo_pci_failed": "lspci çıktısı alınamadı.",

        # MainWindow Logs & Confirmations
        "log_demo_enabled": "[SİSTEM] Demo modu etkinleştirildi.",
        "log_demo_disabled": "[SİSTEM] Demo modu devre dışı bırakıldı.",
        "log_scan_start": "[SİSTEM] Yeni donanım taraması başlatılıyor...",
        "log_scan_done": "[SİSTEM] Donanım ve paket veritabanı taraması tamamlandı.",
        "dialog_install_title": "Sürücü Kurulum Onayı",
        "dialog_install_msg": "<b>{driver_name}</b> paketinin ({package_name}) kurulmasını onaylıyor musunuz?\n\nEk Sürücü Paketleri: {extra}",
        "none_str": "Yok",
        "dialog_remove_title": "Sürücü Kaldırma Onayı",
        "dialog_remove_msg": "<b>{driver_name}</b> paketinin ({package_name}) sistemden kaldırılmasını onaylıyor musunuz?",
        "log_install_req": "[PISI] Kurulum isteği alındı: {pkg}",
        "log_remove_req": "[PISI] Kaldırma isteği alındı: {pkg}",
        "log_repo_req": "[PISI] Depo güncelleme isteği alındı.",
        "version_updated": "Güncel",
        "log_success": "[BAŞARILI] {msg}",
        "dialog_success_title": "İşlem Tamamlandı",
        "log_error": "[HATA] İşlem başarısız: {msg}",
        "dialog_error_title": "İşlem Başarısız",
        "dialog_repo_success_title": "Depolar Güncellendi",
        "dialog_repo_error_title": "Güncelleme Başarısız",

        # Backend Workers / Detectors / Pisi
        "worker_scan_start": "[SİSTEM] Donanım taraması başlatılıyor (lspci & glxinfo)...",
        "worker_scan_count": "[SİSTEM] Toplam {count} adet grafik kartı tespit edildi.",
        "worker_scan_gpu_item": "[DONANIM] {vendor}: {model} (Sürücü: {driver})",
        "worker_pisi_querying": "[PISI] Sürücü paket durumları PiSi veritabanından sorgulanıyor...",
        "worker_pisi_status": "[PISI] {pkg}: Durum -> {status} (Sürüm: {version})",
        "worker_install_success": "{pkg} sürücüsü başarıyla kuruldu!",
        "worker_install_fail": "{pkg} kurulumu başarısız.",
        "worker_remove_success": "{pkg} paketi kaldırıldı!",
        "worker_remove_fail": "{pkg} kaldırma işlemi başarısız.",
        "worker_repo_success": "Depo veritabanı başarıyla güncellendi!",
        "worker_repo_fail": "Depo güncellemesi başarısız.",
        "unknown_vendor": "Bilinmeyen Üretici",
        "unknown_str": "Bilinmiyor",
        "default_str": "Öntanımlı",

        # Pisi Backend messages
        "pisi_install_start": "{pkg_name} paket kurulumu başlatılıyor...",
        "pisi_cmd_install": "[PISI] Kurulum komutu: pisi install {cmd}",
        "pisi_verifying_repos": "[PISI] Depo indeksleri doğrulanıyor...",
        "pisi_downloading": "[PISI] İndiriliyor: {pkg} ({size})",
        "pisi_unpacking": "[PISI] Paket paket açılıyor ve bağımlılıklar kontrol ediliyor...",
        "pisi_copying_files": "[PISI] Sürücü dosyaları kopyalanıyor ve modüller derleniyor...",
        "pisi_updating_xorg": "[PISI] Xorg ve DKMS yapılandırması güncelleniyor...",
        "pisi_install_done": "[PISI] {pkg} başarıyla kuruldu!",
        "pisi_install_comp_msg": "Kurulum başarıyla tamamlandı!",
        "pisi_install_comp_log": "[PISI] İşlem başarıyla tamamlandı.",
        "pisi_err_exit_code": "Hata! Çıkış kodu: {code}",
        "pisi_err_install_fail": "[HATA] pisi install başarısız oldu ({code})",
        "pisi_exception": "[İSTİSNA] {msg}",
        "pisi_remove_start": "{pkg} paketi kaldırılıyor...",
        "pisi_cmd_remove": "[PISI] Kaldırma komutu: pisi remove {pkg}",
        "pisi_checking_deps": "[PISI] Paket bağımlılıkları kontrol ediliyor...",
        "pisi_deleting_files": "[PISI] Sürücü dosyaları sistemden siliniyor...",
        "pisi_refreshing_mods": "[PISI] Sistem modül yapılandırması yenileniyor...",
        "pisi_remove_done": "[PISI] {pkg} paket(ler)i kaldırıldı!",
        "pisi_remove_comp_msg": "Paket kaldırıldı!",
        "pisi_remove_comp_log": "[PISI] Paket başarıyla silindi.",
        "pisi_err_remove_fail": "[HATA] pisi remove başarısız oldu ({code})",
        "pisi_update_repos_start": "Depo veritabanları güncelleniyor...",
        "pisi_cmd_update_repo": "[PISI] pisi update-repo çalıştırılıyor",
        "pisi_downloading_repos": "Depolar indiriliyor...",
        "pisi_updating_repos_log": "[PISI] core, main, contrib depoları güncelleniyor...",
        "pisi_repos_updated_msg": "Depolar güncellendi!",
        "pisi_repos_updated_log": "[PISI] Depo güncelleme tamamlandı.",
    }
}


def tr(key: str, **kwargs) -> str:
    """
    Translate key into active language string.
    If key is not found in active language, fallback to English or the key itself.
    Format with kwargs if provided.
    """
    lang_dict = TRANSLATIONS.get(_ACTIVE_LANG, TRANSLATIONS["en"])
    template = lang_dict.get(key)
    if template is None:
        template = TRANSLATIONS["en"].get(key, key)

    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template
