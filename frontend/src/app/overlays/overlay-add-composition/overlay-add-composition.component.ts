import { Component, EventEmitter, Output } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { BackendService } from '../../services/backend-connection/backend.service';
import { SessionStateService } from '../../services/session-state/session-state.service';
import { GroupInfo } from '../../interfaces';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-overlay-add-composition',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslateModule],
  templateUrl: './overlay-add-composition.component.html',
  styleUrl: './overlay-add-composition.component.css'
})
export class OverlayAddCompositionComponent {
  @Output() close = new EventEmitter<void>()
  @Output() update = new EventEmitter<void>()
  group!: GroupInfo
  addMessage = "..."
  titleInput: string = ""
  authorInput: string = ""
  files: File[] = []

  constructor(private backend: BackendService, private state: SessionStateService) {
    this.state.currentGroup.subscribe((group) => {
      this.group = group;
    });
  }

  onFilesSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      this.files = Array.from(input.files);
    }
  }

  addComposition(): void {
    const compositionData = new FormData()
    compositionData.append('group_id', this.group.group_id.toString())
    compositionData.append('name', this.titleInput)
    compositionData.append('author', this.authorInput)
    this.files.forEach((file) => {
      compositionData.append('files', file);
    });
    this.backend.postRequest('catalogue/addComposition', compositionData).subscribe({
      next: res => {
        this.addMessage = "Composition added"
        this.update.emit()
       },
      error: e => {
        console.log(e)
        this.addMessage = e.detail || "Unexpected error occured."
      }
    })
  }

  closeOverlay() {
    this.close.emit()
  }
}
