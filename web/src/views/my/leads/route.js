import i18n from '~/i18n'
const { t } = i18n.global

export default {
  name: 'MyLeads',
  path: '/my/leads',
  component: () => import('./index.vue'),
  meta: {
    title: '我的线索',
    icon: 'material-symbols:person',
    permission: ['get/api/v1/leads/my'],
    order: 2,
  },
} 