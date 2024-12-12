import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-overlay-join-group',
  standalone: true,
  imports: [],
  templateUrl: './overlay-join-group.component.html',
  styleUrl: './overlay.component.css'
})
export class OverlayJoinGroupComponent {
  @Output() close = new EventEmitter<void>()

  closeOverlay() {
    this.close.emit()
}
}
