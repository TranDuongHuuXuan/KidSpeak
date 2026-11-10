import { studentProfile } from '../data/studentMockData'

const PROFILE_KEY = 'kidspeak-student-account-profile-v1'
const PASSWORD_KEY = 'kidspeak-student-password-demo-v1'
const UPGRADE_KEY = 'kidspeak-student-teacher-upgrade-v1'
const PROFILE_IMAGE_KEY = 'kidspeak-student-profile-image-v1'

const defaultAccount = {
  name: studentProfile.name,
  username: 'minhanh02',
  email: 'minh.anh@kidspeak.vn',
  phone: '0901 234 567',
  birthDate: '2018-05-12',
  gender: 'Nữ',
  address: 'Quận 3, Thành phố Hồ Chí Minh',
  role: 'Học sinh',
  joinedAt: '2026-08-15',
}

function readJson(key, fallback, errorText) {
  try {
    const value = localStorage.getItem(key)
    return value ? JSON.parse(value) : fallback
  } catch (error) {
    throw new Error(errorText, { cause: error })
  }
}

function writeJson(key, value, errorText) {
  try {
    localStorage.setItem(key, JSON.stringify(value))
  } catch (error) {
    throw new Error(errorText, { cause: error })
  }
}

function setCurrentStudent(profile, avatar) {
  const nameParts = profile.name.trim().split(/\s+/)
  const initials = nameParts.length > 1
    ? `${nameParts[0][0]}${nameParts.at(-1)[0]}`.toLocaleUpperCase('vi')
    : nameParts[0].slice(0, 2).toLocaleUpperCase('vi')
  Object.assign(studentProfile, {
    name: profile.name,
    initials,
    avatar,
    role: profile.role,
  })
}

export const studentAccountService = {
  getProfile() {
    const storedProfile = readJson(PROFILE_KEY, defaultAccount, 'Không thể đọc hồ sơ đã lưu.')
    const { avatar: _savedAvatar, ...profile } = storedProfile
    let avatar = ''
    try {
      avatar = localStorage.getItem(PROFILE_IMAGE_KEY) || ''
    } catch (error) {
      throw new Error('Không thể đọc ảnh đại diện đã lưu.', { cause: error })
    }
    setCurrentStudent(profile, avatar)
    return { ...profile, avatar }
  },
  saveProfile(updates) {
    const current = this.getProfile()
    const profile = {
      ...current,
      name: updates.name.trim(),
      phone: updates.phone.trim(),
      birthDate: updates.birthDate,
      gender: updates.gender,
      address: updates.address.trim(),
    }
    const { avatar: _profileAvatar, ...profileData } = profile
    const previousAvatar = current.avatar
    if (updates.avatar !== undefined) {
      try {
        if (updates.avatar) localStorage.setItem(PROFILE_IMAGE_KEY, updates.avatar)
        else localStorage.removeItem(PROFILE_IMAGE_KEY)
      } catch (error) {
        throw new Error('Không thể lưu ảnh đại diện. Hãy chọn ảnh nhỏ hơn.', { cause: error })
      }
    }
    try {
      writeJson(PROFILE_KEY, profileData, 'Không thể lưu hồ sơ vào trình duyệt.')
    } catch (error) {
      if (updates.avatar !== undefined) {
        try {
          if (previousAvatar) localStorage.setItem(PROFILE_IMAGE_KEY, previousAvatar)
          else localStorage.removeItem(PROFILE_IMAGE_KEY)
        } catch (rollbackError) {
          throw new Error('Không thể lưu hồ sơ, đồng thời không khôi phục được ảnh đại diện.', { cause: rollbackError })
        }
      }
      throw error
    }
    setCurrentStudent(profile, updates.avatar ?? current.avatar)
    return { ...profile, avatar: updates.avatar ?? current.avatar }
  },
  updatePassword(currentPassword, newPassword) {
    let storedPassword
    try {
      storedPassword = localStorage.getItem(PASSWORD_KEY) || 'Kidspeak123!'
    } catch (error) {
      throw new Error('Không thể đọc mật khẩu mô phỏng.', { cause: error })
    }
    if (currentPassword !== storedPassword) throw new Error('Mật khẩu hiện tại chưa chính xác.')
    try {
      localStorage.setItem(PASSWORD_KEY, newPassword)
    } catch (error) {
      throw new Error('Không thể cập nhật mật khẩu mô phỏng.', { cause: error })
    }
  },
  getUpgradeHistory() {
    return readJson(UPGRADE_KEY, [], 'Không thể tải lịch sử yêu cầu nâng cấp.')
  },
  submitUpgradeRequest(details) {
    const history = this.getUpgradeHistory()
    const pending = history.find((request) => request.status === 'pending')
    if (pending) throw new Error('Bạn đang có yêu cầu chờ xét duyệt.')
    const profile = this.getProfile()
    if (profile.role === 'Giảng viên') throw new Error('Tài khoản của bạn đã là giảng viên.')
    const request = {
      id: `UPG-${new Date().toISOString().slice(0, 10).replaceAll('-', '')}-${String(Date.now()).slice(-5)}`,
      submittedAt: new Date().toISOString(),
      reviewedAt: null,
      status: 'pending',
      note: '',
      details: { ...details, submittedPhone: profile.phone },
      evidenceFiles: details.evidenceFiles.map(({ name, size, type }) => ({ name, size, type })),
    }
    history.unshift(request)
    writeJson(UPGRADE_KEY, history, 'Không thể lưu yêu cầu nâng cấp vào trình duyệt.')
    return request
  },
  reviewUpgradeRequest(requestId, status, note = '') {
    if (!['approved', 'rejected'].includes(status)) throw new TypeError('Trạng thái xét duyệt không hợp lệ.')
    const history = this.getUpgradeHistory()
    const request = history.find((item) => item.id === requestId)
    if (!request) throw new Error('Không tìm thấy yêu cầu nâng cấp.')
    if (request.status !== 'pending') throw new Error('Yêu cầu này đã được xử lý.')
    request.status = status
    request.reviewedAt = new Date().toISOString()
    request.note = note
    writeJson(UPGRADE_KEY, history, 'Không thể cập nhật trạng thái yêu cầu.')
    if (status === 'approved') {
      const profile = this.getProfile()
      profile.role = 'Giảng viên'
      const { avatar: _profileAvatar, ...profileData } = profile
      writeJson(PROFILE_KEY, profileData, 'Không thể cập nhật vai trò demo.')
      setCurrentStudent(profile, profile.avatar)
    }
    return request
  },
}
