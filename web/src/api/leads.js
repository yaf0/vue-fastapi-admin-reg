import request from '@/utils/request'

export default {
  // 获取线索列表
  getLeadList(params) {
    return request.get('/api/v1/leads/list', { params })
  },

  // 获取我的线索
  getMyLeads(params) {
    return request.get('/api/v1/leads/my', { params })
  },

  // 创建线索
  createLead(data) {
    return request.post('/api/v1/leads/create', data)
  },

  // 批量创建线索
  batchCreateLeads(data) {
    return request.post('/api/v1/leads/batch_create', data)
  },

  // 批量分配线索
  batchAssignLeads(data) {
    return request.post('/api/v1/leads/batch_assign', data)
  },

  // 更新线索
  updateLead(data) {
    return request.post('/api/v1/leads/update', data)
  },

  // 删除线索
  deleteLead(params) {
    return request.delete('/api/v1/leads/delete', { params })
  },

  // 标记为已读
  markAsRead(data) {
    return request.post('/api/v1/leads/mark_read', data)
  },

  // 标记为未读
  markAsUnread(data) {
    return request.post('/api/v1/leads/mark_unread', data)
  }
} 