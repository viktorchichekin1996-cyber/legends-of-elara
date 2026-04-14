import { useState } from 'react';
import {
  View,
  Panel,
  PanelHeader,
  Group,
  FormItem,
  Input,
  Select,
  Button,
  Text,
  ScreenSpinner,
  Snackbar,
  Div,
  Card,
} from '@vkontakte/vkui';
import { Icon28ErrorCircleOutline } from '@vkontakte/icons';
import { useCharacterStore } from '../store/characterStore';
import { CHARACTER_CLASSES, CharacterClass } from '../types/character';

interface CreateCharacterScreenProps {
  id: string;
}

// Опции для Select
const classOptions = CHARACTER_CLASSES.map((c) => ({
  value: c.value,
  label: c.label,
}));

export function CreateCharacterScreen({ id }: CreateCharacterScreenProps) {
  const { createCharacter, isLoading, error, clearError } = useCharacterStore();
  const [name, setName] = useState('');
  const [selectedClass, setSelectedClass] = useState<CharacterClass>('воин');
  const [nameError, setNameError] = useState('');

  const handleSubmit = async () => {
    setNameError('');
    
    // Валидация имени
    if (!name.trim()) {
      setNameError('Введите имя персонажа');
      return;
    }
    if (name.length < 3) {
      setNameError('Имя должно содержать минимум 3 символа');
      return;
    }
    if (name.length > 50) {
      setNameError('Имя слишком длинное');
      return;
    }

    try {
      await createCharacter({ name: name.trim(), character_class: selectedClass });
    } catch {
      // Ошибка уже сохранена в сторе
    }
  };

  const selectedClassInfo = CHARACTER_CLASSES.find((c) => c.value === selectedClass);

  return (
    <View activePanel={id}>
      <Panel id={id}>
        <PanelHeader>Создание персонажа</PanelHeader>
        
        {/* ScreenSpinner без пропса text */}
        {isLoading && <ScreenSpinner />}

        {error && (
          <Snackbar
            before={<Icon28ErrorCircleOutline fill="var(--vkui--color_icon_negative)" />}
            onClose={clearError}
            onClosed={clearError}
          >
            {error}
          </Snackbar>
        )}

        <Group>
          <Div style={{ textAlign: 'center', marginBottom: 16 }}>
            <Text style={{ fontSize: 48 }}>🐉</Text>
            <Text weight="2" style={{ fontSize: 18 }}>
              Добро пожаловать в Легенды Элары!
            </Text>
            <Text style={{ color: 'var(--vkui--color_text_secondary)' }}>
              Создайте своего героя и отправляйтесь в приключение.
            </Text>
          </Div>

          <FormItem
            top="Имя персонажа"
            bottom={nameError}
            status={nameError ? 'error' : 'default'}
          >
            <Input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Введите имя"
              maxLength={50}
              disabled={isLoading}
            />
          </FormItem>

          <FormItem top="Класс">
            {/* Select с пропом options */}
            <Select
              value={selectedClass}
              onChange={(e) => setSelectedClass(e.target.value as CharacterClass)}
              options={classOptions}
              disabled={isLoading}
            />
          </FormItem>

          {selectedClassInfo && (
            <Card mode="shadow" style={{ margin: '0 0 16px' }}>
              <Div>
                <Text weight="2">{selectedClassInfo.label}</Text>
                <Text style={{ color: 'var(--vkui--color_text_secondary)', fontSize: 14 }}>
                  {selectedClassInfo.description}
                </Text>
              </Div>
            </Card>
          )}

          <FormItem>
            <Button
              size="l"
              stretched
              onClick={handleSubmit}
              disabled={isLoading || !name.trim()}
              loading={isLoading}
            >
              Создать персонажа
            </Button>
          </FormItem>
        </Group>
      </Panel>
    </View>
  );
}