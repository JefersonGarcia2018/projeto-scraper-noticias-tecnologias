const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'login', component: () => import('pages/LoginPage.vue') }
    ]
  },
  {
    path: '/admin',
    component: () => import('layouts/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', component: () => import('pages/admin/AdminHome.vue') },
      { path: 'scraper', component: () => import('pages/admin/AdminScraper.vue') },
      { path: 'users/create', component: () => import('pages/admin/AdminUserCreate.vue') },
      { path: 'users/list', component: () => import('pages/admin/AdminUserList.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
