import { Component, OnInit } from '@angular/core';
import { AdminService, Admin } from '../../../../domains/services/admin.services'; 

@Component({
  selector: 'app-admin-page',
  templateUrl: './admin-page.component.html',
  styleUrls: ['./admin-page.component.css']
})

export class AdminPageComponent implements OnInit {
  users: Admin[] = [];

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.adminService.getAdmins().subscribe({
      next: (data) => {
        this.users = data; 
        console.log('Данные для админки успешно загружены!', data);
      },
      error: (err) => {
        console.error('Не удалось загрузить данные:', err);
      }
    });
  }

  deleteUser(id: number): void {
    if (confirm('Удалить пользователя?')) {
      this.adminService.deleteAdmin(id).subscribe({
        next: () => {
          console.log('Пользователь успешно удален на сервере');
          this.loadUsers(); 
        },
        error: (err) => console.error('Ошибка удаления:', err)
      });
    }
  }
}

