import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-overlay-choose-group',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './overlay-choose-group.component.html',
  styleUrl: './overlay.component.css'
})
export class OverlayChooseGroupComponent {
  @Output() close = new EventEmitter<void>()
  userGroups = ["HELL", "WHY", "DUM DUM DUM"]

  chooseGroup(e: MouseEvent): void {
    const chosen = e.target as HTMLElement
  }

  closeOverlay() {
    this.close.emit()
}
}
