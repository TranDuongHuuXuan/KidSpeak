import { initialStudentConversations } from '../data/studentMessagesMockData'

const STORAGE_KEY = 'kidspeak-student-messages-v1'

function cloneConversations(conversations) {
  return conversations.map((conversation) => ({
    ...conversation,
    messages: conversation.messages.map((message) => ({ ...message })),
  }))
}

function readConversations() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return cloneConversations(initialStudentConversations)
    const conversations = JSON.parse(stored)
    if (!Array.isArray(conversations) || conversations.some((item) => !item.id || !Array.isArray(item.messages))) {
      throw new Error('Dữ liệu hội thoại không đúng định dạng.')
    }
    return conversations
  } catch (error) {
    throw new Error('Không thể tải tin nhắn đã lưu trên trình duyệt.', { cause: error })
  }
}

function writeConversations(conversations) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations))
  } catch (error) {
    throw new Error('Không thể lưu tin nhắn vào trình duyệt.', { cause: error })
  }
}

export const studentMessagingService = {
  list() {
    return readConversations().sort((a, b) => {
      const lastA = a.messages.at(-1)?.sentAt || ''
      const lastB = b.messages.at(-1)?.sentAt || ''
      return lastB.localeCompare(lastA)
    })
  },
  markRead(conversationId) {
    const conversations = readConversations()
    const conversation = conversations.find((item) => item.id === conversationId)
    if (!conversation) throw new Error('Không tìm thấy hội thoại.')
    conversation.unread = 0
    conversation.messages.forEach((message) => {
      if (message.from === 'other') message.status = 'read'
    })
    writeConversations(conversations)
    return conversation
  },
  toggleUnread(conversationId) {
    const conversations = readConversations()
    const conversation = conversations.find((item) => item.id === conversationId)
    if (!conversation) throw new Error('Không tìm thấy hội thoại.')
    conversation.unread = conversation.unread > 0 ? 0 : 1
    writeConversations(conversations)
    return conversation
  },
  send(conversationId, content) {
    const text = content.trim()
    if (!text) throw new Error('Hãy nhập nội dung tin nhắn.')
    const conversations = readConversations()
    const conversation = conversations.find((item) => item.id === conversationId)
    if (!conversation) throw new Error('Không tìm thấy hội thoại.')
    const message = {
      id: `me-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      from: 'me',
      text,
      sentAt: new Date().toISOString(),
      status: 'sent',
    }
    conversation.messages.push(message)
    conversation.unread = 0
    writeConversations(conversations)
    return { conversation, message }
  },
}
