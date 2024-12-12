import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-overlay-create-group',
  standalone: true,
  imports: [],
  templateUrl: './overlay-create-group.component.html',
  styleUrl: './overlay.component.css'
})
export class OverlayCreateGroupComponent {
  @Output() close = new EventEmitter<void>()

  closeOverlay() {
    this.close.emit()
}
}
