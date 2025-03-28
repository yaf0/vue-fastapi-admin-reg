import i18n from '~/i18n'
const { t } = i18n.global

export default {
  name: 'Lead',
  path: '/system/lead',
  component: () => import('./index.vue'),
  meta: {
    title: '线索管理',
    icon: 'material-symbols:person-search',
    permission: ['get/api/v1/leads/list'],
    order: 3,
  },
} 