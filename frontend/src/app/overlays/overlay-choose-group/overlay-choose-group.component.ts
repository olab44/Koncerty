import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-overlay-choose-group',
  standalone: true,
  imports: [CommonModule, TranslateModule],
  templateUrl: './overlay-choose-group.component.html',
  styleUrl: './overlay-choose-group.component.css'
})
export class OverlayChooseGroupComponent {
  constructor(private router: Router) {}

  @Output() close = new EventEmitter<void>()
  userGroups = [
    { id: 1, name: 'ORKIESTRA PRUSZKÓW', role: 'admin' },
    { id: 2, name: 'CHÓR UW', role: 'reg' },
    { id: 3, name: 'ZESPÓŁ PIEŚNI I TAŃCA', isAdmin: 'coord' }
  ];

  chooseGroup(group: any): void {
    this.router.navigate(['group'], {state: {group}});
  }

  closeOverlay() {
    this.close.emit()
}
}
