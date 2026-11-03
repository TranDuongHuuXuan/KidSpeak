<template>
  <main class="flex min-h-screen flex-col items-center justify-center gap-4 bg-kids-bg px-6 text-center text-kids-text">
    <p class="text-7xl font-extrabold text-kids-primary">404</p>
    <h1 class="text-2xl font-bold">Không tìm thấy trang</h1>
    <p>Đường dẫn này không tồn tại hoặc đã được thay đổi.</p>
    <RouterLink
      :to="{ name: 'Login' }"
      class="rounded-xl bg-kids-cta px-5 py-3 font-semibold text-white transition hover:brightness-95"
    >
      Về trang đăng nhập
    </RouterLink>
  </main>
</template>
