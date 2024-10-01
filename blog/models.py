from django.db import models


class Post(models.Model):
    '''данные о посте '''
    title = models.CharField('Заголовок записи', max_length=100)
    description = models.TextField('Текс записи')
    author = models.CharField('Имя автора', max_length=100)
    date = models.DateField('Дата публикации')
    img = models.ImageField('Картинки', upload_to='image/%Y')



    def __str__(self):
        return f'{self.title}, {self.author}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date']

class Comments(models.Model):
    '''Комментарии'''
    email = models.EmailField()
    name = models.CharField('Имя', max_length=50)
    text_comments = models.TextField('Текст комментария', max_length=2000)
    post = models.ForeignKey(Post, verbose_name='Публикация', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.post}' # что выводится в админке

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Likes(models.Model):
    '''лайки'''
    ip = models.CharField('IP-адрес', max_length=100)
    pos = models.ForeignKey(Post, verbose_name='Публикация', on_delete=models.CASCADE)

