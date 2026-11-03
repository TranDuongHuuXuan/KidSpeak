import { reactive, ref } from 'vue'

export const adminData = reactive({
  users: [
    { id: 0, name: 'Admin KidSpeak', email: 'admin@kidspeak.vn', role: 'Admin', joinedAt: '2026-01-01', status: 'Active' },
    { id: 1, name: 'Nguyễn Minh Anh', email: 'minhanh@example.com', role: 'Student', joinedAt: '2026-10-28', status: 'Active' },
    { id: 2, name: 'Trần Thị Mai', email: 'mai.tran@example.com', role: 'Teacher', joinedAt: '2026-10-26', status: 'Active' },
    { id: 3, name: 'Lê Gia Bảo', email: 'giabao@example.com', role: 'Student', joinedAt: '2026-10-24', status: 'Pending' },
    { id: 4, name: 'Phạm Hoàng Yến', email: 'yen.pham@example.com', role: 'Teacher', joinedAt: '2026-10-20', status: 'Active' },
    { id: 5, name: 'Đỗ Khánh Linh', email: 'khanhlinh@example.com', role: 'Student', joinedAt: '2026-10-18', status: 'Locked' },
    { id: 6, name: 'Nguyễn Quốc Bảo', email: 'quocbao@example.com', role: 'Student', joinedAt: '2026-10-15', status: 'Active' },
    { id: 7, name: 'Vũ Thanh Hà', email: 'thanhha@example.com', role: 'Teacher', joinedAt: '2026-10-12', status: 'Pending' },
    { id: 8, name: 'Bùi Đức Minh', email: 'ducminh@example.com', role: 'Student', joinedAt: '2026-10-09', status: 'Active' },
    { id: 9, name: 'Hoàng Thu Trang', email: 'trang.hoang@example.com', role: 'Teacher', joinedAt: '2026-10-05', status: 'Active' },
    { id: 10, name: 'Mai Tuấn Kiệt', email: 'tuan.kiet@example.com', role: 'Student', joinedAt: '2026-10-02', status: 'Active' },
    { id: 11, name: 'Đặng Ngọc Hà', email: 'ngoc.ha@example.com', role: 'Student', joinedAt: '2026-09-29', status: 'Active' },
    { id: 12, name: 'Nguyễn Hải Đăng', email: 'haidang@example.com', role: 'Student', joinedAt: '2026-09-26', status: 'Pending' },
  ],
  roles: [
    { id: 1, name: 'Admin', description: 'Toàn quyền quản trị hệ thống.', permissions: { users: true, lessons: true, viewLessons: true, notifications: true } },
    { id: 2, name: 'Teacher', description: 'Tạo và quản lý nội dung bài học.', permissions: { users: false, lessons: true, viewLessons: true, notifications: false } },
    { id: 3, name: 'Student', description: 'Học tập và luyện phát âm.', permissions: { users: false, lessons: false, viewLessons: true, notifications: false } },
    { id: 4, name: 'Guest', description: 'Trải nghiệm các bài học công khai.', permissions: { users: false, lessons: false, viewLessons: true, notifications: false } },
  ],
  teacherRequests: [
    {
      id: 1,
      name: 'Nguyễn Thị Lan',
      email: 'lan.nguyen@example.com',
      sentAt: '2026-11-02',
      status: 'Pending',
      phone: '0901 234 567',
      dateOfBirth: '1992-04-15',
      address: 'Quận Cầu Giấy, Hà Nội',
      specialization: 'Giáo dục mầm non, phát triển ngôn ngữ',
      education: 'Đại học Sư phạm Hà Nội',
      document: 'Chứng chỉ sư phạm mầm non',
      experience: '5 năm giảng dạy tiếng Việt cho trẻ.',
      certificates: [
        { name: 'Cử nhân Giáo dục Mầm non', issuer: 'Đại học Sư phạm Hà Nội', year: 2015, status: 'Đã cung cấp' },
        { name: 'Chứng chỉ nghiệp vụ sư phạm', issuer: 'Trường Đại học Giáo dục', year: 2017, status: 'Đã cung cấp' },
      ],
    },
    {
      id: 2,
      name: 'Trần Văn Minh',
      email: 'minh.tran@example.com',
      sentAt: '2026-11-01',
      status: 'Pending',
      phone: '0912 345 678',
      dateOfBirth: '1989-09-22',
      address: 'Quận Hải Châu, Đà Nẵng',
      specialization: 'Ngôn ngữ học ứng dụng, luyện phát âm',
      education: 'Đại học Khoa học Xã hội và Nhân văn',
      document: 'Bằng cử nhân Ngôn ngữ học',
      experience: '3 năm hướng dẫn phát âm.',
      certificates: [
        { name: 'Cử nhân Ngôn ngữ học', issuer: 'Đại học KHXH&NV - ĐHQG TP.HCM', year: 2012, status: 'Đã cung cấp' },
        { name: 'Chứng chỉ giảng dạy tiếng Việt', issuer: 'Trung tâm Ngôn ngữ học ứng dụng', year: 2018, status: 'Đã cung cấp' },
      ],
    },
    {
      id: 3,
      name: 'Lê Thu Hương',
      email: 'huong.le@example.com',
      sentAt: '2026-10-28',
      status: 'Approved',
      phone: '0934 567 890',
      dateOfBirth: '1987-02-10',
      address: 'Quận Thanh Xuân, Hà Nội',
      specialization: 'Giáo dục tiểu học, tiếng Việt',
      education: 'Đại học Giáo dục - ĐHQG Hà Nội',
      document: 'Chứng chỉ giáo viên tiểu học',
      experience: '7 năm giảng dạy tiểu học.',
      certificates: [
        { name: 'Cử nhân Giáo dục Tiểu học', issuer: 'Đại học Giáo dục - ĐHQG Hà Nội', year: 2009, status: 'Đã xác thực' },
        { name: 'Chứng chỉ bồi dưỡng giáo viên tiểu học', issuer: 'Sở Giáo dục và Đào tạo Hà Nội', year: 2019, status: 'Đã xác thực' },
      ],
    },
    {
      id: 4,
      name: 'Phạm Quốc Huy',
      email: 'huy.pham@example.com',
      sentAt: '2026-10-25',
      status: 'Rejected',
      phone: '0987 654 321',
      dateOfBirth: '1994-12-03',
      address: 'Quận Ninh Kiều, Cần Thơ',
      specialization: 'Hỗ trợ phát triển ngôn ngữ',
      education: 'Cao đẳng Sư phạm Cần Thơ',
      document: 'Hồ sơ đang bổ sung',
      experience: 'Đang hoàn thiện hồ sơ xác thực.',
      certificates: [
        { name: 'Bằng Cao đẳng Sư phạm', issuer: 'Cao đẳng Sư phạm Cần Thơ', year: 2016, status: 'Cần bổ sung bản sao rõ nét' },
      ],
      rejectionReason: 'Vui lòng bổ sung bản sao bằng cấp rõ nét.',
    },
  ],
  lessons: [
    { id: 1, title: 'Bé làm quen với âm M', teacher: 'Trần Thị Mai', topic: 'Âm đầu', submittedAt: '2026-11-02', status: 'Pending', description: 'Bài học giúp bé nhận biết và luyện phát âm âm M qua các từ quen thuộc.', image: '🐱', vocabulary: ['mèo', 'mẹ', 'mũ'], guide: 'Khép nhẹ hai môi, phát âm /m/ và cảm nhận âm rung ở mũi.', audio: 'Đã có audio mẫu', note: '' },
    { id: 2, title: 'Thế giới động vật quanh bé', teacher: 'Phạm Hoàng Yến', topic: 'Từ vựng', submittedAt: '2026-11-01', status: 'Pending', description: 'Cùng khám phá tên gọi các con vật gần gũi.', image: '🐻', vocabulary: ['mèo', 'chó', 'thỏ'], guide: 'Nghe mẫu, quan sát khẩu hình và đọc rõ từng tiếng.', audio: 'Chưa có audio', note: '' },
    { id: 3, title: 'Phân biệt âm S và X', teacher: 'Trần Thị Mai', topic: 'Âm đầu', submittedAt: '2026-10-29', status: 'Approved', description: 'Luyện phân biệt hai âm đầu thường gặp.', image: '🗣️', vocabulary: ['sao', 'xe', 'sách'], guide: 'Đặt lưỡi nhẹ phía sau răng, hơi thoát đều.', audio: 'Đã có audio mẫu', note: '' },
    { id: 4, title: 'Bé tập nói lời chào', teacher: 'Nguyễn Thị Lan', topic: 'Giao tiếp', submittedAt: '2026-10-27', status: 'Rejected', description: 'Thực hành các lời chào thường dùng.', image: '👋', vocabulary: ['xin chào', 'tạm biệt'], guide: 'Nói chậm, rõ và giữ giọng tự nhiên.', audio: 'Chưa có audio', note: 'Vui lòng bổ sung hình minh họa cho bài học.' },
  ],
  notifications: [
    { id: 1, title: 'Chào mừng đến với KidSpeak', content: 'Khám phá các bài học phát âm mới mỗi ngày nhé!', audience: 'Tất cả người dùng', type: 'Hệ thống', createdAt: '2026-11-01', status: 'Sent' },
    { id: 2, title: 'Cập nhật hướng dẫn tạo bài học', content: 'Giáo viên vui lòng xem lại hướng dẫn gửi bài học mới.', audience: 'Giáo viên', type: 'Cập nhật', createdAt: '2026-10-30', status: 'Draft' },
    { id: 3, title: 'Thử thách phát âm tuần này', content: 'Cùng luyện 5 từ mới và chia sẻ kết quả nhé!', audience: 'Học viên', type: 'Sự kiện', createdAt: '2026-10-28', status: 'Sent' },
  ],
  settings: {
    systemName: 'KidSpeak',
    description: 'Hệ thống hỗ trợ trẻ em luyện tập và cải thiện khả năng phát âm.',
    contactEmail: 'support@kidspeak.vn',
    allowRegistration: true,
    allowLogin: true,
    requireVerification: true,
    passwordLength: 8,
    sessionMinutes: 60,
    maintenanceMode: false,
    systemNotifications: true,
  },
})

export const defaultSettings = Object.freeze({ ...adminData.settings })
export const toastMessage = ref('')
let toastTimer

export function notify(message) {
  toastMessage.value = message
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastMessage.value = ''
  }, 2800)
}

export function formatDate(date) {
  return new Intl.DateTimeFormat('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' }).format(new Date(`${date}T00:00:00`))
}
