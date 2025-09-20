export async function login(phone, password) {
    console.log(import.meta.env.BASE_URL);
    const res = await fetch(import.meta.env.BASE_URL + 'users.json', { cache: 'no-store' });
    console.log(res);
    if (!res.ok) throw new Error('Failed to load users.json');
    const data = await res.json();
    const user = (data.users || []).find(u => u.phone === phone && u.password === password);
    if (!user) throw new Error('Invalid credentials');
    // Mock storing token
    const token = btoa(`${user.phone}:${Date.now()}`);
    localStorage.setItem('auth_token', token);
    localStorage.setItem('auth_name', user.displayName);
    localStorage.setItem('auth_user_id', user.id);
    return { token, name: user.displayName};
  }
  
  export function isAuthed() {
    return !!localStorage.getItem('auth_token');
  }
  
  export function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_name');
  }

  export function getUserId() {
    return parseInt(localStorage.getItem('auth_user_id'));
  }