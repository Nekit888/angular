export interface Admin {
    admin_id?: number;
    admin_login: string;
    admin_password_hash?: string;
    is_active_admin?: number;
    admin_birth_date?: string;
    created_at?: string;
}