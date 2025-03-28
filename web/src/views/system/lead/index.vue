<script setup>
import { h, onMounted, ref } from 'vue'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NSpace,
  NTag,
  NPopconfirm,
  NUpload,
  NMessage,
} from 'naive-ui'
import { useUserStore } from '@/store'
import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import { formatDate, renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'
import TheIcon from '@/components/icon/TheIcon.vue'

defineOptions({ name: '线索管理' })

const $table = ref(null)
const queryItems = ref({})
const userStore = useUserStore()

const {
  modalVisible,
  modalTitle,
  modalAction,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: '线索',
  initForm: {},
  doCreate: api.createLead,
  doUpdate: api.updateLead,
  doDelete: api.deleteLead,
  refresh: () => $table.value?.handleSearch(),
})

const userOptions = ref([])

onMounted(() => {
  $table.value?.handleSearch()
  api.getUserList({ page: 1, page_size: 9999 }).then((res) => (userOptions.value = res.data))
})

const columns = [
  {
    title: '时间',
    key: 'time',
    width: 160,
    align: 'center',
    render(row) {
      return formatDate(row.time)
    },
  },
  {
    title: '号码',
    key: 'phone',
    width: 120,
    align: 'center',
  },
  {
    title: '微信',
    key: 'wechat',
    width: 120,
    align: 'center',
  },
  {
    title: '备注',
    key: 'remark',
    width: 200,
    align: 'center',
  },
  {
    title: '意向等级',
    key: 'intention_level',
    width: 100,
    align: 'center',
    render(row) {
      const colors = ['red', 'orange', 'yellow', 'green', 'blue']
      return h(NTag, { type: colors[row.intention_level - 1] }, { default: () => row.intention_level })
    },
  },
  {
    title: '是否已读',
    key: 'is_read',
    width: 100,
    align: 'center',
    render(row) {
      return h(NTag, { type: row.is_read ? 'success' : 'warning' }, { default: () => row.is_read ? '已读' : '未读' })
    },
  },
  {
    title: '分配用户',
    key: 'assigned_user',
    width: 120,
    align: 'center',
    render(row) {
      const user = userOptions.value.find(u => u.id === row.assigned_user_id)
      return user ? user.username : '-'
    },
  },
  {
    title: '操作',
    key: 'actions',
    width: 200,
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        h(
          NButton,
          {
            size: 'small',
            type: 'primary',
            style: 'margin-right: 8px;',
            onClick: () => handleEdit(row),
          },
          {
            default: () => '编辑',
            icon: renderIcon('material-symbols:edit', { size: 16 }),
          }
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ lead_id: row.id }, false),
            onNegativeClick: () => {},
          },
          {
            trigger: () =>
              h(
                NButton,
                {
                  size: 'small',
                  type: 'error',
                  style: 'margin-right: 8px;',
                },
                {
                  default: () => '删除',
                  icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                }
              ),
            default: () => h('div', {}, '确定删除该线索吗?'),
          }
        ),
      ]
    },
  },
]

const handleUpload = async ({ file }) => {
  try {
    const reader = new FileReader()
    reader.onload = async (e) => {
      const content = e.target.result
      const lines = content.split('\n')
      const leads = lines.map(line => {
        const [time, phone, wechat, remark, intention_level, assigned_user_id] = line.split(',')
        return {
          time: new Date(time),
          phone,
          wechat,
          remark,
          intention_level: parseInt(intention_level),
          assigned_user_id: parseInt(assigned_user_id),
        }
      })
      await api.batchCreateLeads({ leads })
      NMessage.success('批量导入成功')
      $table.value?.handleSearch()
    }
    reader.readAsText(file.file)
  } catch (error) {
    NMessage.error('批量导入失败：' + error.message)
  }
}

const handleBatchAssign = async (user_id) => {
  const selectedRows = $table.value?.getSelectedRows() || []
  if (selectedRows.length === 0) {
    NMessage.warning('请选择要分配的线索')
    return
  }
  try {
    await api.batchAssignLeads({
      lead_ids: selectedRows.map(row => row.id),
      assigned_user_id: user_id,
    })
    NMessage.success('批量分配成功')
    $table.value?.handleSearch()
  } catch (error) {
    NMessage.error('批量分配失败：' + error.message)
  }
}

const validateLead = {
  time: [
    {
      required: true,
      message: '请选择时间',
      trigger: ['input', 'blur'],
    },
  ],
  phone: [
    {
      required: true,
      message: '请输入号码',
      trigger: ['input', 'blur'],
    },
  ],
  wechat: [
    {
      required: true,
      message: '请输入微信',
      trigger: ['input', 'blur'],
    },
  ],
  intention_level: [
    {
      required: true,
      message: '请选择意向等级',
      trigger: ['input', 'blur', 'change'],
    },
    {
      type: 'number',
      min: 1,
      max: 5,
      message: '意向等级必须在1-5之间',
      trigger: ['input', 'blur', 'change'],
    },
  ],
  assigned_user_id: [
    {
      required: true,
      message: '请选择分配用户',
      trigger: ['input', 'blur', 'change'],
    },
  ],
}
</script>

<template>
  <CommonPage show-footer title="线索列表">
    <template #action>
      <NSpace>
        <NButton type="primary" @click="handleAdd">
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建线索
        </NButton>
        <NUpload
          accept=".csv,.txt"
          :show-file-list="false"
          :custom-request="handleUpload"
        >
          <NButton type="info">
            <TheIcon icon="material-symbols:upload-file" :size="18" class="mr-5" />批量导入
          </NButton>
        </NUpload>
        <NSelect
          v-model:value="selectedUser"
          :options="userOptions.map(u => ({ label: u.username, value: u.id }))"
          placeholder="选择分配用户"
          style="width: 200px"
        />
        <NButton type="warning" @click="handleBatchAssign(selectedUser)">
          <TheIcon icon="material-symbols:group" :size="18" class="mr-5" />批量分配
        </NButton>
      </NSpace>
    </template>
    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getLeadList"
      row-key="id"
      :row-selection="true"
    >
      <template #queryBar>
        <QueryBarItem label="号码" :label-width="40">
          <NInput
            v-model:value="queryItems.phone"
            clearable
            type="text"
            placeholder="请输入号码"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="微信" :label-width="40">
          <NInput
            v-model:value="queryItems.wechat"
            clearable
            type="text"
            placeholder="请输入微信"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="已读" :label-width="40">
          <NSelect
            v-model:value="queryItems.is_read"
            :options="[
              { label: '已读', value: true },
              { label: '未读', value: false },
            ]"
            clearable
            placeholder="请选择"
            style="width: 120px"
          />
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- 新增/编辑 弹窗 -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
        :rules="validateLead"
      >
        <NFormItem label="时间" path="time">
          <NInput
            v-model:value="modalForm.time"
            type="datetime-local"
            clearable
          />
        </NFormItem>
        <NFormItem label="号码" path="phone">
          <NInput v-model:value="modalForm.phone" clearable placeholder="请输入号码" />
        </NFormItem>
        <NFormItem label="微信" path="wechat">
          <NInput v-model:value="modalForm.wechat" clearable placeholder="请输入微信" />
        </NFormItem>
        <NFormItem label="备注" path="remark">
          <NInput
            v-model:value="modalForm.remark"
            type="textarea"
            clearable
            placeholder="请输入备注"
          />
        </NFormItem>
        <NFormItem label="意向等级" path="intention_level">
          <NSelect
            v-model:value="modalForm.intention_level"
            :options="[
              { label: '1级', value: 1 },
              { label: '2级', value: 2 },
              { label: '3级', value: 3 },
              { label: '4级', value: 4 },
              { label: '5级', value: 5 },
            ]"
            clearable
            placeholder="请选择意向等级"
          />
        </NFormItem>
        <NFormItem label="分配用户" path="assigned_user_id">
          <NSelect
            v-model:value="modalForm.assigned_user_id"
            :options="userOptions.map(u => ({ label: u.username, value: u.id }))"
            clearable
            placeholder="请选择分配用户"
          />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template> 