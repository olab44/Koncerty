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
  @Output() refresh = new EventEmitter<void>();
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
    const compositionData: any = {
      parent_group: this.group.group_id,
      name: this.titleInput,
      author: this.authorInput,
      files: []
    };
    if (this.files && this.files.length > 0) {
      this.files.forEach((file: File) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          const base64File = reader.result as string;
  
          compositionData.files.push({
            name: file.name,
            content: base64File.split(',')[1]
          });
          if (compositionData.files.length === this.files.length) {
            this.sendCompositionData(compositionData);
          }
        };
        reader.readAsDataURL(file);
      });
    } else {
      this.sendCompositionData(compositionData);
    }
  }
  
  sendCompositionData(compositionData: any): void {
    this.backend.postRequest('catalogue/addComposition', compositionData).subscribe({
      next: res => {
        this.addMessage = "Composition added";
        this.refresh.emit();
      },
      error: e => {
        console.log(e);
        this.addMessage = e.detail || "Unexpected error occurred.";
      }
    });
  }
  

  closeOverlay() {
    this.close.emit()
  }
}
