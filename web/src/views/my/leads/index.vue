<script setup>
import { h, onMounted, ref } from 'vue'
import {
  NButton,
  NInput,
  NSelect,
  NSpace,
  NTag,
  NMessage,
} from 'naive-ui'
import { useUserStore } from '@/store'
import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import { formatDate, renderIcon } from '@/utils'
import api from '@/api'

defineOptions({ name: '我的线索' })

const $table = ref(null)
const queryItems = ref({})
const userStore = useUserStore()

onMounted(() => {
  $table.value?.handleSearch()
})

const columns = [
  {
    title: '时间',
    key: 'time',
    width: 160,
    align: 'center',
    render(row) {
      return h(
        NButton,
        {
          size: 'small',
          type: 'text',
          ghost: true,
          onClick: () => handleCopy(formatDate(row.time)),
        },
        {
          default: () => formatDate(row.time),
          icon: renderIcon('material-symbols:content-copy', { size: 16 }),
        }
      )
    },
  },
  {
    title: '号码',
    key: 'phone',
    width: 120,
    align: 'center',
    render(row) {
      return h(
        NButton,
        {
          size: 'small',
          type: 'text',
          ghost: true,
          onClick: () => handleCopy(row.phone),
        },
        {
          default: () => row.phone,
          icon: renderIcon('material-symbols:content-copy', { size: 16 }),
        }
      )
    },
  },
  {
    title: '微信',
    key: 'wechat',
    width: 120,
    align: 'center',
    render(row) {
      return h(
        NButton,
        {
          size: 'small',
          type: 'text',
          ghost: true,
          onClick: () => handleCopy(row.wechat),
        },
        {
          default: () => row.wechat,
          icon: renderIcon('material-symbols:content-copy', { size: 16 }),
        }
      )
    },
  },
  {
    title: '备注',
    key: 'remark',
    width: 200,
    align: 'center',
    render(row) {
      return h(
        NButton,
        {
          size: 'small',
          type: 'text',
          ghost: true,
          onClick: () => handleCopy(row.remark),
        },
        {
          default: () => row.remark || '-',
          icon: renderIcon('material-symbols:content-copy', { size: 16 }),
        }
      )
    },
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
      return h(
        NSpace,
        { justify: 'center' },
        {
          default: () => [
            h(NTag, { type: row.is_read ? 'success' : 'warning' }, { default: () => row.is_read ? '已读' : '未读' }),
            !row.is_read && h(
              NButton,
              {
                size: 'tiny',
                type: 'primary',
                onClick: () => handleMarkAsRead(row.id),
              },
              { default: () => '标为已读' }
            ),
            row.is_read && h(
              NButton,
              {
                size: 'tiny',
                type: 'warning',
                onClick: () => handleMarkAsUnread(row.id),
              },
              { default: () => '标为未读' }
            ),
          ],
        }
      )
    },
  },
]

const handleCopy = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    NMessage.success('复制成功')
  } catch (error) {
    NMessage.error('复制失败')
  }
}

const handleMarkAsRead = async (id) => {
  try {
    await api.markAsRead({ lead_id: id })
    NMessage.success('标记成功')
    $table.value?.handleSearch()
  } catch (error) {
    NMessage.error('标记失败：' + error.message)
  }
}

const handleMarkAsUnread = async (id) => {
  try {
    await api.markAsUnread({ lead_id: id })
    NMessage.success('标记成功')
    $table.value?.handleSearch()
  } catch (error) {
    NMessage.error('标记失败：' + error.message)
  }
}
</script>

<template>
  <CommonPage show-footer title="我的线索">
    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getMyLeads"
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
  </CommonPage>
</template> 