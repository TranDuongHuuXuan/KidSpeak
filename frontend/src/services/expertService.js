import { expertData } from '../data/expertMockData'
import { toast } from '../composable/useToast'

let nextId = 1

export function notifyExpert(message, tone = 'success') {
  toast[tone === 'error' ? 'error' : 'success'](message)
}

export const expertService = {
  create(collection, record) {
    const item = { ...record, id: `${collection.slice(0, 3).toUpperCase()}-${String(Date.now()).slice(-5)}${nextId++}` }
    expertData[collection].unshift(item)
    return item
  },
  update(collection, id, updates) {
    const index = expertData[collection].findIndex((item) => item.id === id)
    if (index < 0) throw new Error(`Không tìm thấy dữ liệu ${id}.`)
    Object.assign(expertData[collection][index], updates)
    return expertData[collection][index]
  },
  remove(collection, id) {
    const index = expertData[collection].findIndex((item) => item.id === id)
    if (index < 0) throw new Error(`Không tìm thấy dữ liệu ${id}.`)
    expertData[collection].splice(index, 1)
  },
  sendMessage(studentId, text) {
    const conversation = expertData.conversations.find((item) => item.studentId === studentId)
    if (!conversation) throw new Error('Không tìm thấy hội thoại.')
    const message = {
      id: Date.now(),
      from: 'expert',
      text,
      time: new Intl.DateTimeFormat('vi-VN', { hour: '2-digit', minute: '2-digit' }).format(new Date()),
    }
    conversation.messages.push(message)
    conversation.preview = text
    conversation.time = message.time
    return message
  },
}
