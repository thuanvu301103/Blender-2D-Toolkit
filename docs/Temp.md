#: 1
Đoạn: Xác định mặt phẳng → chỉ số trục
Dòng: 165-168
Hàm đề xuất: resolve_axis_indices(context)
Ghi chú: Trả [2]/[1]/[0] cho waving, còn sliding trả (0,1), (0,2), (1,2). Đây là
điểm khác nhau chính giữa hai loại. Nên đưa thành hook.
────────────────────────────────────────
#: 2
Đoạn: Tính danh sách offsets
Dòng: 174-178
Hàm đề xuất: get_offsets(context)
Ghi chú: Đang hard-code scene.idle_waving_angle. Cần là hook, vì sliding dùng
distance và vector hướng.
────────────────────────────────────────
#: 3
Đoạn: Đảm bảo rotation mode hợp lệ
Dòng: 180-185
Hàm đề xuất: ensure_euler_rotation_mode(target)
Ghi chú: Chỉ waving cần, sliding không cần. Nên là bước riêng hoặc hook rỗng mặc
định.
────────────────────────────────────────
#: 4
Đoạn: Tạo animation_data + action
Dòng: 194-204
Hàm đề xuất: ensure_action(target_obj, pose_bone)
Ghi chú: Giống hệt nhau ở hai loại, chỉ khác hậu tố WavingAction/SlidingAction.
Thêm hook get_action_suffix().
────────────────────────────────────────
#: 5
Đoạn: Lấy animated_target, data_path
Dòng: 181, 188-192
Hàm đề xuất: resolve_animated_target(target_obj, pose_bone, prop)
Ghi chú: Trả (animated_target, data_path). prop là "rotation_euler" hoặc
"location", qua hook get_property_name().
────────────────────────────────────────
#: 6
Đoạn: Vòng chèn keyframe
Dòng: 207-215
Hàm đề xuất: insert_keyframes(animated_target, prop, axis_indices, frames,
offsets, base_value)
Ghi chú: Phần cốt lõi. Waving đổi 1 trục, sliding đổi 2 trục theo offset *
unit_vector.
────────────────────────────────────────
#: 7
Đoạn: Thông báo kết quả
Dòng: 231-235
Hàm đề xuất: report_done(target_obj, pose_bone)
Ghi chú: Gần như giống nhau, chỉ cần tên loại animation.